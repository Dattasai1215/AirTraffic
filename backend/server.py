import os
import time
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from backend.opensky_fetcher import fetch_active_flights
from backend.weather_engine import get_weather_zones, check_weather_effects
from backend.collision_detector import calculate_separation, predict_collision_risk
from backend.anomaly_detector import detect_anomaly
from backend.flight_predictor import predict_future_position

try:
    import openai
except ImportError:
    openai = None

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
if openai and OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

current_flights = []
last_update = 0.0

MAX_FLIGHTS = 120


def safe_predict_position(flight, storm_dist):
    try:
        return predict_future_position(flight, storm_dist)
    except Exception:
        heading_rad = flight.get("heading", 0.0) * 3.14159265 / 180.0
        dt = 30.0
        delta_lat = (flight.get("velocity", 0.0) * dt * __import__("math").cos(heading_rad)) / 111000.0
        delta_lon = (flight.get("velocity", 0.0) * dt * __import__("math").sin(heading_rad)) / (111000.0 * max(0.1, __import__("math").cos(flight.get("latitude", 0.0) * 3.14159265 / 180.0)))
        return (
            float(flight.get("latitude", 0.0) + delta_lat),
            float(flight.get("longitude", 0.0) + delta_lon),
            float(min(13000.0, max(100.0, flight.get("altitude", 0.0) + flight.get("vertical_rate", 0.0) * dt)))
        )


def generate_ai_summary(total_flights, conflict_count, anomaly_count, active_alerts):
    fallback = (
        f"Live tracking active for {total_flights} flights. "
        f"Detected {conflict_count} potential conflict{'' if conflict_count == 1 else 's'} and {anomaly_count} anomaly{'' if anomaly_count == 1 else 'ies'}. "
        f"Top alert: {active_alerts[0] if active_alerts else 'No active alerts'}.")

    if not openai or not OPENAI_API_KEY:
        return fallback

    try:
        prompt = (
            "You are an air traffic control assistant. "
            "Summarize the current airspace status in 2-3 concise sentences. "
            "Focus on the number of flights, conflicts, anomalies, and any urgent alert details. "
            f"Total flights: {total_flights}. Conflicts: {conflict_count}. Anomalies: {anomaly_count}. "
            f"Recent alerts: {', '.join(active_alerts[:3]) if active_alerts else 'None'}.")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an air traffic control operations assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=120,
            temperature=0.6
        )
        summary = response.choices[0].message.content.strip()
        return summary or fallback
    except Exception as exc:
        logging.warning("OpenAI summary generation failed: %s", exc)
        return fallback


@app.route("/api/flights", methods=["GET"])
def api_flights():
    global current_flights, last_update
    current_flights = fetch_active_flights(current_flights, dt=5.0)
    last_update = time.time()

    if len(current_flights) > MAX_FLIGHTS:
        current_flights = current_flights[:MAX_FLIGHTS]

    weather_zones = get_weather_zones(last_update)
    flights_payload = []
    alerts = []
    conflicts = []
    anomaly_count = 0

    for flight in current_flights:
        storm_dist, storm_threat = check_weather_effects(
            flight.get("latitude", 0.0),
            flight.get("longitude", 0.0),
            flight.get("altitude", 0.0)
        )

        future_lat, future_lon, future_alt = safe_predict_position(flight, storm_dist)
        is_anomaly, anomaly_score = detect_anomaly(flight)
        if is_anomaly:
            anomaly_count += 1
            alerts.append(f"Anomaly detected for {flight.get('callsign', flight.get('icao24'))} (score {anomaly_score:.2f})")

        flights_payload.append({
            **flight,
            "storm_distance_km": round(storm_dist, 2),
            "storm_threat": storm_threat,
            "predicted_latitude": round(future_lat, 5),
            "predicted_longitude": round(future_lon, 5),
            "predicted_altitude": round(future_alt, 1),
            "is_anomaly": is_anomaly,
            "anomaly_score": round(anomaly_score, 3),
        })

    for idx, flight in enumerate(flights_payload):
        if len(conflicts) > 30:
            break
        for other in flights_payload[idx + 1:]:
            dist_h, dist_v = calculate_separation(flight, other)
            threat_dist = min(flight["storm_distance_km"], other["storm_distance_km"])
            risk = predict_collision_risk(flight, other, dist_h, dist_v, threat_dist)
            if risk >= 0.5 or (dist_h < 3.0 and dist_v < 600.0):
                conflicts.append({
                    "flight1": flight["callsign"],
                    "flight2": other["callsign"],
                    "distance_km": round(dist_h, 2),
                    "vertical_sep_m": round(dist_v, 1),
                    "risk": round(risk, 3)
                })
                alerts.append(
                    f"Conflict risk {risk:.2f} between {flight.get('callsign')} and {other.get('callsign')}"
                )

    if not alerts:
        alerts.append("Airspace is stable with no urgent alerts.")

    summary = generate_ai_summary(
        total_flights=len(flights_payload),
        conflict_count=len(conflicts),
        anomaly_count=anomaly_count,
        active_alerts=alerts
    )

    return jsonify({
        "flights": flights_payload,
        "weather_zones": weather_zones,
        "conflictCount": len(conflicts),
        "summary": summary,
        "alerts": alerts,
        "timestamp": int(last_update)
    })


@app.route("/api/status", methods=["GET"])
def api_status():
    return jsonify({
        "status": "ok",
        "timestamp": int(time.time()),
        "mode": "backend-api"
    })


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    app.run(host=host, port=port, debug=False)
