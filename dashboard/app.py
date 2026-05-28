import sys
import os
import time
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.opensky_fetcher import fetch_active_flights, LAMIN, LAMAX, LOMIN, LOMAX
from backend.weather_engine import get_weather_zones, check_weather_effects
from backend.flight_predictor import predict_future_position
from backend.anomaly_detector import detect_anomaly
from backend.collision_detector import calculate_separation, predict_collision_risk
from alerts.collision_alert import get_alert

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(layout="wide", page_title="AeroShield ATC - AI Air Traffic Collision Prediction")

# ---------------------------------
# ATC THEME STYLING
# ---------------------------------
st.markdown("""
<style>
/* Dark ATC theme */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at center, #020617, #09090b);
    color: #f8fafc;
}
[data-testid="stSidebar"] {
    background-color: #0f172a;
    border-right: 1px solid #1e293b;
}
h1, h2, h3, h4, h5, h6 {
    color: #e2e8f0;
}
.title-header {
    background: linear-gradient(90deg, #0f172a, #1e293b, #0f172a);
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #334155;
    text-align: center;
    margin-bottom: 25px;
}
.title-header h1 {
    color: #22d3ee;
    font-size: 36px;
    font-weight: 800;
    letter-spacing: 2px;
    margin: 0;
    text-shadow: 0 0 10px rgba(34, 211, 238, 0.3);
}
.title-header p {
    color: #94a3b8;
    margin: 5px 0 0 0;
    font-size: 14px;
    text-transform: uppercase;
}
.metric-container {
    display: flex;
    justify-content: space-between;
    gap: 15px;
    margin-bottom: 20px;
}
.metric-card {
    background: rgba(15, 23, 42, 0.6);
    backdrop-filter: blur(10px);
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 15px;
    flex: 1;
    text-align: center;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.metric-card.critical {
    border-left: 4px solid #ef4444;
}
.metric-card.warning {
    border-left: 4px solid #f59e0b;
}
.metric-card.info {
    border-left: 4px solid #06b6d4;
}
.metric-card.success {
    border-left: 4px solid #10b981;
}
.metric-val {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 5px;
}
.metric-val.cyan { color: #22d3ee; }
.metric-val.red { color: #f87171; }
.metric-val.orange { color: #fb923c; }
.metric-val.purple { color: #c084fc; }

.metric-label {
    font-size: 11px;
    text-transform: uppercase;
    color: #64748b;
    letter-spacing: 1px;
}
.console-box {
    background-color: #020617;
    border: 1px solid #1e293b;
    border-radius: 8px;
    font-family: 'Courier New', Courier, monospace;
    padding: 12px;
    height: 180px;
    overflow-y: auto;
    color: #22c55e;
    font-size: 12px;
    line-height: 1.5;
}
.console-line {
    margin-bottom: 4px;
}
.console-timestamp {
    color: #64748b;
}
.info-card {
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 15px;
}
.flight-row-critical {
    background-color: rgba(220, 38, 38, 0.15);
    border-left: 4px solid #dc2626;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# INITIALIZE STATE
# ---------------------------------
if "flights" not in st.session_state:
    st.session_state.flights = []
if "time_tick" not in st.session_state:
    st.session_state.time_tick = 0
if "logs" not in st.session_state:
    st.session_state.logs = [
        f"[{datetime.now().strftime('%H:%M:%S')}] AERO-SHIELD: Air Traffic Control prediction engine initialized.",
        f"[{datetime.now().strftime('%H:%M:%S')}] XGBoost: Loaded flight path trajectory regressors.",
        f"[{datetime.now().strftime('%H:%M:%S')}] Isolation Forest: Loaded aviation anomaly detector."
    ]

# Rerun trigger
st.session_state.time_tick += 1
dt = 5.0  # seconds between updates

# Add system log helper
def add_log(msg):
    ts = datetime.now().strftime('%H:%M:%S')
    st.session_state.logs.append(f"[{ts}] {msg}")
    if len(st.session_state.logs) > 30:
        st.session_state.logs.pop(0)

# Fetch current flights
with st.spinner("Retrieving aircraft vectors..."):
    st.session_state.flights = fetch_active_flights(st.session_state.flights, dt=dt)

active_flights = st.session_state.flights
num_flights = len(active_flights)

# Get weather cells
weather_cells = get_weather_zones(st.session_state.time_tick * 5.0)

# ---------------------------------
# PROCESS FLIGHTS & APPLY ML
# ---------------------------------
anomalous_flights = []
flight_coordinates = {}
predictions = {}

for f in active_flights:
    # 1. Proximity to storms
    min_storm_dist, storm_threat = check_weather_effects(f["latitude"], f["longitude"], f["altitude"])
    f["storm_dist"] = min_storm_dist
    f["storm_threat"] = storm_threat
    
    # 2. Anomaly Detection
    # Generate a dummy heading rate for mock flights (minor drift)
    heading_rate = np.random.uniform(0.0, 1.2) if f.get("is_mock", False) else abs(f["vertical_rate"]) * 0.1
    is_anom, anom_score = detect_anomaly(f, heading_rate)
    f["is_anomaly"] = is_anom
    f["anomaly_score"] = anom_score
    if is_anom:
        anomalous_flights.append(f)
        
    # 3. XGBoost Trajectory Predictor
    pred_lat, pred_lon, pred_alt = predict_future_position(f, min_storm_dist)
    f["pred_latitude"] = pred_lat
    f["pred_longitude"] = pred_lon
    f["pred_altitude"] = pred_alt
    
    # Store for pairwise operations
    flight_coordinates[f["icao24"]] = (f["latitude"], f["longitude"], f["altitude"])
    predictions[f["icao24"]] = (pred_lat, pred_lon, pred_alt)

# 4. Pairwise Collision Classifier
conflicts = []
checked_pairs = set()

for i in range(num_flights):
    for j in range(i+1, num_flights):
        f1 = active_flights[i]
        f2 = active_flights[j]
        
        # Calculate separation distance
        dist_h, dist_v = calculate_separation(f1, f2)
        
        # If reasonably close, classify collision risk
        if dist_h < 30.0 and dist_v < 1000.0:
            avg_storm_dist = min(f1["storm_dist"], f2["storm_dist"])
            risk_prob = predict_collision_risk(f1, f2, dist_h, dist_v, avg_storm_dist)
            
            if risk_prob > 0.15:
                conflicts.append({
                    "f1": f1,
                    "f2": f2,
                    "prob": risk_prob,
                    "dist_h": dist_h,
                    "dist_v": dist_v
                })

# Assign risk levels to flights
for f in active_flights:
    f["max_risk"] = 0.0
    f["conflict_partner"] = None

for c in conflicts:
    f1, f2, prob = c["f1"], c["f2"], c["prob"]
    if prob > f1["max_risk"]:
        f1["max_risk"] = prob
        f1["conflict_partner"] = f2["callsign"]
    if prob > f2["max_risk"]:
        f2["max_risk"] = prob
        f2["conflict_partner"] = f1["callsign"]

# Sort conflicts by severity
conflicts = sorted(conflicts, key=lambda x: x["prob"], reverse=True)

# Generate system log notifications dynamically
if len(conflicts) > 0:
    worst = conflicts[0]
    add_log(f"Conflict Warning: {worst['f1']['callsign']} & {worst['f2']['callsign']} closing. Risk: {worst['prob']*100:.1f}%.")
if len(anomalous_flights) > 0:
    new_anom = anomalous_flights[0]
    add_log(f"Anomaly detected: {new_anom['callsign']} (Squawk {new_anom['squawk']}) flagged by Isolation Forest.")

# ---------------------------------
# RENDER LAYOUT
# ---------------------------------
# Header banner
st.markdown("""
<div class="title-header">
    <h1>✈️ AEROSHIELD</h1>
    <p>AI Air Traffic Conflict Prediction & Airspace Monitoring System</p>
</div>
""", unsafe_allow_html=True)

# Metrics Grid
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.markdown(f"""
    <div class="metric-card info">
        <div class="metric-val cyan">{num_flights}</div>
        <div class="metric-label">Surveillance Fleet</div>
    </div>
    """, unsafe_allow_html=True)

with metric_col2:
    critical_conflicts = sum(1 for c in conflicts if c["prob"] > 0.75)
    card_type = "critical" if critical_conflicts > 0 else ("warning" if len(conflicts) > 0 else "success")
    val_color = "red" if critical_conflicts > 0 else ("orange" if len(conflicts) > 0 else "cyan")
    st.markdown(f"""
    <div class="metric-card {card_type}">
        <div class="metric-val {val_color}">{len(conflicts)}</div>
        <div class="metric-label">Active Airspace Conflicts</div>
    </div>
    """, unsafe_allow_html=True)

with metric_col3:
    anom_card = "critical" if len(anomalous_flights) > 0 else "success"
    anom_color = "purple" if len(anomalous_flights) > 0 else "cyan"
    st.markdown(f"""
    <div class="metric-card {anom_card}">
        <div class="metric-val {anom_color}">{len(anomalous_flights)}</div>
        <div class="metric-label">Telemetry Anomalies</div>
    </div>
    """, unsafe_allow_html=True)

with metric_col4:
    weather_threats = sum(1 for f in active_flights if f["storm_threat"] != "None")
    weather_card = "warning" if weather_threats > 0 else "success"
    weather_color = "orange" if weather_threats > 0 else "cyan"
    st.markdown(f"""
    <div class="metric-card {weather_card}">
        <div class="metric-val {weather_color}">{weather_threats}</div>
        <div class="metric-label">Aircraft in Storm Cells</div>
    </div>
    """, unsafe_allow_html=True)

# Main Section
col_main, col_side = st.columns([3, 1])

# 3D Graph
with col_main:
    # ---------------------------------
    # BUILD 3D PLOTLY FIGURE
    # ---------------------------------
    fig = go.Figure()
    
    # 1. Add Weather storm cell spheres
    for cell in weather_cells:
        sc_lat = cell["latitude"]
        sc_lon = cell["longitude"]
        sc_alt = cell["altitude"]
        r_km = cell["radius_km"]
        
        r_lat = r_km / 111.0
        r_lon = r_km / (111.0 * np.cos(np.radians(sc_lat)))
        r_alt = r_km * 1000.0  # in meters
        
        u = np.linspace(0, 2*np.pi, 25)
        v = np.linspace(0, np.pi, 25)
        xs = sc_lon + r_lon * np.outer(np.sin(v), np.cos(u))
        ys = sc_lat + r_lat * np.outer(np.sin(v), np.sin(u))
        zs = sc_alt + r_alt * np.outer(np.cos(v), np.ones_like(u))
        
        fig.add_trace(go.Surface(
            x=xs, y=ys, z=zs,
            colorscale=[[0, cell["color"]], [1, cell["color"]]],
            showscale=False,
            opacity=0.15,
            name=cell["name"],
            hoverinfo="text",
            hovertext=f"⛈️ {cell['name']} ({cell['severity']})<br>Radius: {r_km} km<br>Alt: {sc_alt}m"
        ))
        
    # 2. Add grid floor for airspace mapping
    grid_lats = np.linspace(LAMIN, LAMAX, 10)
    grid_lons = np.linspace(LOMIN, LOMAX, 10)
    for glat in grid_lats:
        fig.add_trace(go.Scatter3d(
            x=grid_lons, y=[glat]*10, z=[0]*10,
            mode="lines", line=dict(color="#1e293b", width=1),
            showlegend=False, hoverinfo="none"
        ))
    for glon in grid_lons:
        fig.add_trace(go.Scatter3d(
            x=[glon]*10, y=grid_lats, z=[0]*10,
            mode="lines", line=dict(color="#1e293b", width=1),
            showlegend=False, hoverinfo="none"
        ))

    # 3. Add aircraft markers
    xs_ac, ys_ac, zs_ac = [], [], []
    colors_ac, sizes_ac, text_ac, symbols_ac = [], [], [], []
    
    for f in active_flights:
        xs_ac.append(f["longitude"])
        ys_ac.append(f["latitude"])
        zs_ac.append(f["altitude"])
        
        # Color coding by risk and anomaly
        alert_info = get_alert(f["max_risk"])
        if f["is_anomaly"]:
            color = "#d946ef" # Neon Magenta
            symbol = "diamond"
            size = 9
            status_text = "ANOMALY FLAGGED"
        else:
            symbol = "circle"
            size = 7
            if alert_info["level"] == "CRITICAL":
                color = "#ef4444" # Red
                status_text = "CRITICAL CONFLICT (RA)"
            elif alert_info["level"] == "WARNING":
                color = "#f97316" # Orange
                status_text = "TRAFFIC ADVISORY"
            elif alert_info["level"] == "MONITOR":
                color = "#eab308" # Yellow
                status_text = "PROXIMITY WARNING"
            else:
                color = "#10b981" # Green
                status_text = "SAFE SEPARATION"
                
        colors_ac.append(color)
        sizes_ac.append(size)
        symbols_ac.append(symbol)
        
        text_ac.append(
            f"<b>✈️ {f['callsign']}</b> ({f['origin_country']})<br>"
            f"Status: {status_text}<br>"
            f"Alt: {f['altitude']:.0f} m | Speed: {f['velocity']:.1f} m/s<br>"
            f"Squawk: {f['squawk']}<br>"
            f"Storm Proximity: {f['storm_dist']:.1f} km"
        )
        
        # Draw Trajectory Projection Vectors (XGBoost Predictions)
        fig.add_trace(go.Scatter3d(
            x=[f["longitude"], f["pred_longitude"]],
            y=[f["latitude"], f["pred_latitude"]],
            z=[f["altitude"], f["pred_altitude"]],
            mode="lines+markers",
            line=dict(color=color, width=3, dash="dash"),
            marker=dict(size=[0, 3], color=color),
            showlegend=False,
            hoverinfo="none"
        ))

    # Plot the aircraft markers
    fig.add_trace(go.Scatter3d(
        x=xs_ac, y=ys_ac, z=zs_ac,
        mode="markers",
        marker=dict(
            size=sizes_ac,
            color=colors_ac,
            symbol=symbols_ac,
            line=dict(color="#09090b", width=1)
        ),
        text=text_ac,
        hoverinfo="text",
        name="Surveillance Fleet"
    ))
    
    # 4. Add Conflict warning lines
    for c in conflicts:
        f1, f2, prob = c["f1"], c["f2"], c["prob"]
        # Only draw if threat is significant
        line_color = "rgba(239, 68, 68, 0.8)" if prob > 0.75 else "rgba(249, 115, 22, 0.6)"
        fig.add_trace(go.Scatter3d(
            x=[f1["longitude"], f2["longitude"]],
            y=[f1["latitude"], f2["latitude"]],
            z=[f1["altitude"], f2["altitude"]],
            mode="lines",
            line=dict(color=line_color, width=4),
            showlegend=False,
            hoverinfo="text",
            hovertext=f"⚠️ Airspace Conflict Risk: {prob*100:.1f}%<br>Sep: {c['dist_h']:.2f} km | {c['dist_v']:.0f}m"
        ))
        
    fig.update_layout(
        scene=dict(
            xaxis=dict(
                title="Longitude", 
                backgroundcolor="#020617", 
                gridcolor="#1e293b", 
                showbackground=True,
                range=[LOMIN, LOMAX]
            ),
            yaxis=dict(
                title="Latitude", 
                backgroundcolor="#020617", 
                gridcolor="#1e293b", 
                showbackground=True,
                range=[LAMIN, LAMAX]
            ),
            zaxis=dict(
                title="Altitude (meters)", 
                backgroundcolor="#020617", 
                gridcolor="#1e293b", 
                showbackground=True,
                range=[0, 13000]
            ),
            aspectratio=dict(x=1.2, y=1.2, z=0.7),
            bgcolor="black"
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        height=650,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Sidebar / Flight Control Inspector
with col_side:
    st.markdown("### 🔍 Aircraft Inspector")
    
    # Select flight
    flight_names = sorted([f["callsign"] for f in active_flights])
    selected_callsign = st.selectbox("Select Flight to Track:", ["None"] + flight_names)
    
    if selected_callsign != "None":
        f = next(flight for flight in active_flights if flight["callsign"] == selected_callsign)
        alert_info = get_alert(f["max_risk"])
        
        status_color = "red" if f["is_anomaly"] else alert_info["color"]
        status_lbl = "ANOMALY DETECTED" if f["is_anomaly"] else alert_info["msg"]
        
        st.markdown(f"""
        <div class="info-card" style="border-left: 5px solid {status_color}">
            <h4>✈️ {f['callsign']}</h4>
            <p><b>ICAO24:</b> {f['icao24']}</p>
            <p><b>Reg Country:</b> {f['origin_country']}</p>
            <hr style="border: 0; border-top: 1px solid #334155; margin: 10px 0;">
            <p><b>Altitude:</b> {f['altitude']:.0f} m (~{(f['altitude']*3.28084):.0f} ft)</p>
            <p><b>Velocity:</b> {f['velocity']:.1f} m/s (~{(f['velocity']*1.94384):.1f} kts)</p>
            <p><b>Heading:</b> {f['heading']:.0f}° | Rate: {f.get('vertical_rate', 0.0):.1f} m/s</p>
            <p><b>Transponder Squawk:</b> <span style="font-family: monospace; color: #22d3ee;">{f['squawk']}</span></p>
            <hr style="border: 0; border-top: 1px solid #334155; margin: 10px 0;">
            <p><b>ML Status:</b> <span style="color:{status_color}; font-weight:bold;">{status_lbl}</span></p>
            <p><b>Collision Risk Prob:</b> {f['max_risk']*100:.1f}%</p>
            {f"<p><b>Conflict Partner:</b> {f['conflict_partner']}</p>" if f['conflict_partner'] else ""}
            <p><b>Storm Dist:</b> {f['storm_dist']:.1f} km ({f['storm_threat']})</p>
            <p><b>Isolation Forest Anomaly Score:</b> {f['anomaly_score']:.3f}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Select an aircraft from the dropdown to view real-time flight telemetry and ML diagnostics.")
        
    st.markdown("### 📻 ATC Console Log")
    console_content = ""
    for log in reversed(st.session_state.logs):
        console_content += f"<div class='console-line'>{log}</div>"
        
    st.markdown(f"""
    <div class="console-box">
        {console_content}
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------
# SECTOR TRAFFIC VIEW (TABLE)
# ---------------------------------
st.markdown("### 📋 Sector Surveillance Report")
report_rows = []
for f in active_flights:
    alert_info = get_alert(f["max_risk"])
    status = "🚨 ANOMALY" if f["is_anomaly"] else f"{alert_info['icon']} {alert_info['level']}"
    
    report_rows.append({
        "Callsign": f["callsign"],
        "Country": f["origin_country"],
        "Latitude": f"{f['latitude']:.4f}",
        "Longitude": f"{f['longitude']:.4f}",
        "Altitude (m)": f"{f['altitude']:.0f}",
        "Speed (m/s)": f"{f['velocity']:.1f}",
        "Squawk": f["squawk"],
        "Status": status,
        "Max Conflict Risk": f"{f['max_risk']*100:.1f}%",
        "Storm Dist (km)": f"{f['storm_dist']:.1f}"
    })
    
st.dataframe(pd.DataFrame(report_rows), use_container_width=True)

# ---------------------------------
# SIMULATED INTERACTIVE RERUN
# ---------------------------------
time.sleep(5)
st.rerun()