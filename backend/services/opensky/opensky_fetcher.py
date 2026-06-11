import requests
import random
import numpy as np

# JFK / NY Airspace boundary
LAMIN = 39.5
LAMAX = 41.5
LOMIN = -75.0
LOMAX = -72.0

OPENSKY_URL = f"https://opensky-network.org/api/states/all?lamin={LAMIN}&lamax={LAMAX}&lomin={LOMIN}&lomax={LOMAX}"

# Mock airline carrier prefixes
CALLSIGN_PREFIXES = ["AAL", "DAL", "UAL", "JBU", "SWA", "FDX", "UPS", "BAW", "DLH", "AFR"]

def generate_mock_flight(icao_idx):
    icao24 = f"a{random.randint(100000, 999999):06x}"
    carrier = random.choice(CALLSIGN_PREFIXES)
    flight_num = random.randint(100, 9999)
    callsign = f"{carrier}{flight_num:<4}".strip()
    
    # Randomly assign emergency squawk to 1% of simulated flights to test anomaly detection
    rand_val = random.random()
    if rand_val < 0.008:
        squawk = "7700"  # Emergency
    elif rand_val < 0.012:
        squawk = "7600"  # Radio failure
    elif rand_val < 0.015:
        squawk = "7500"  # Hijack
    else:
        squawk = str(random.choice([1200, 2000, 4321, 5678]))
        
    return {
        "icao24": icao24,
        "callsign": callsign,
        "origin_country": random.choice(["United States", "United Kingdom", "Germany", "France", "Canada"]),
        "longitude": random.uniform(LOMIN, LOMAX),
        "latitude": random.uniform(LAMIN, LAMAX),
        "altitude": random.uniform(1000, 11000),      # meters
        "velocity": random.uniform(120, 260),         # m/s
        "heading": random.uniform(0, 360),            # degrees
        "vertical_rate": random.uniform(-10, 10),      # m/s
        "squawk": squawk,
        "is_mock": True
    }

def fetch_active_flights(prev_flights=None, dt=5.0):
    """
    Fetches real-time flight vectors from OpenSky Network, or falls back to
    generating/updating mock flights in the New York airspace.
    """
    try:
        import os
        username = os.getenv("OPENSKY_CLIENT_ID") or os.getenv("OPENSKY_USERNAME")
        password = os.getenv("OPENSKY_CLIENT_SECRET") or os.getenv("OPENSKY_PASSWORD")
        auth = (username, password) if username and password else None

        # Try fetching real data (timeout quickly to prevent UI lags)
        if auth:
            response = requests.get(OPENSKY_URL, auth=auth, timeout=2.5)
        else:
            response = requests.get(OPENSKY_URL, timeout=2.5)
        if response.status_code == 200:
            data = response.json()
            states = data.get("states")
            if states:
                flights = []
                for s in states[:150]:  # Limit to 150 flights for rendering efficiency
                    # OpenSky fields:
                    # 0: icao24, 1: callsign, 2: origin, 5: lon, 6: lat, 7: altitude (m), 9: velocity (m/s), 10: heading, 11: vertical_rate (m/s), 14: squawk
                    if s[5] is not None and s[6] is not None:
                        flights.append({
                            "icao24": s[0],
                            "callsign": (s[1] or "UNK").strip(),
                            "origin_country": s[2],
                            "longitude": float(s[5]),
                            "latitude": float(s[6]),
                            "altitude": float(s[7] or 3000.0),
                            "velocity": float(s[9] or 180.0),
                            "heading": float(s[10] or 0.0),
                            "vertical_rate": float(s[11] or 0.0),
                            "squawk": str(s[14] or "2000"),
                            "is_mock": False
                        })
                if flights:
                    return flights
    except Exception:
        # Ignore errors and fall back to simulation
        pass

    # High-fidelity mock simulator update/generation
    if not prev_flights:
        # Initial population of 25 aircraft
        return [generate_mock_flight(i) for i in range(25)]
    
    updated_flights = []
    for f in prev_flights:
        # Only keep mock flights or simulate them if we lost API connection
        if not f.get("is_mock", False):
            # If we were previously showing real flights, they might disappear on rate-limit, 
            # so let's convert them to mock to avoid a sudden blank screen
            f["is_mock"] = True
            
        # Update flight position based on velocity and heading
        rad_heading = np.radians(f["heading"])
        
        # 1 deg lat ~ 111,000 meters. 1 deg lon ~ 111,000 * cos(lat) meters.
        delta_lat = (f["velocity"] * np.cos(rad_heading) * dt) / 111000.0
        delta_lon = (f["velocity"] * np.sin(rad_heading) * dt) / (111000.0 * np.cos(np.radians(f["latitude"])))
        delta_alt = f["vertical_rate"] * dt
        
        f["latitude"] += delta_lat
        f["longitude"] += delta_lon
        f["altitude"] += delta_alt
        
        # Add slight random adjustments to make flight paths dynamic
        f["heading"] = (f["heading"] + random.uniform(-3, 3)) % 360
        f["velocity"] = np.clip(f["velocity"] + random.uniform(-1, 1), 100, 280)
        f["vertical_rate"] = np.clip(f["vertical_rate"] + random.uniform(-0.5, 0.5), -15, 15)
        
        # Boundaries check - respawn planes that fly out of the sector
        if (f["latitude"] < LAMIN or f["latitude"] > LAMAX or 
            f["longitude"] < LOMIN or f["longitude"] > LOMAX or 
            f["altitude"] < 200 or f["altitude"] > 13000):
            # Respawn flight at a random border
            f = generate_mock_flight(0)
            
        updated_flights.append(f)
        
    return updated_flights
