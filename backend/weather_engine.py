import numpy as np

# Static/slowly drifting weather systems in the JFK airspace sector
WEATHER_CELLS = [
    {
        "id": "storm_alpha",
        "name": "Supercell Alpha",
        "latitude": 40.25,
        "longitude": -74.20,
        "altitude": 6000.0,       # center altitude in meters
        "radius_km": 18.0,
        "severity": "Severe Storm (Red)",
        "color": "rgba(239, 68, 68, 0.35)", # semi-transparent red
        "line_color": "rgba(239, 68, 68, 0.8)"
    },
    {
        "id": "turb_beta",
        "name": "Turbulence Cell Beta",
        "latitude": 41.10,
        "longitude": -73.10,
        "altitude": 8000.0,
        "radius_km": 22.0,
        "severity": "Heavy Turbulence (Orange)",
        "color": "rgba(245, 158, 11, 0.3)", # semi-transparent orange
        "line_color": "rgba(245, 158, 11, 0.7)"
    }
]

def get_weather_zones(t=None):
    """
    Returns active weather zones. Optionally drifts them slightly over time.
    """
    if t is not None:
        # Add a small drift over time (t in seconds)
        drifting_cells = []
        for cell in WEATHER_CELLS:
            c = cell.copy()
            # Drift east-northeast at ~0.0001 degrees per second
            c["latitude"] += np.sin(t * 0.01) * 0.02
            c["longitude"] += np.cos(t * 0.01) * 0.02
            drifting_cells.append(c)
        return drifting_cells
    return WEATHER_CELLS

def get_distance_to_storm(lat, lon, alt, storm):
    """
    Computes 3D distance between aircraft and storm center in kilometers.
    """
    # Horizontal distance in km
    dx = (lat - storm["latitude"]) * 111.0
    dy = (lon - storm["longitude"]) * 111.0 * np.cos(np.radians(lat))
    dist_h = np.sqrt(dx**2 + dy**2)
    
    # Vertical distance in km (convert alt in meters to km)
    dist_v = abs(alt - storm["altitude"]) / 1000.0
    
    return np.sqrt(dist_h**2 + dist_v**2)

def check_weather_effects(lat, lon, alt):
    """
    Returns minimum distance to any storm cell and the name of the cell if inside it.
    """
    min_dist = 999.0
    active_threat = "None"
    
    for storm in WEATHER_CELLS:
        d = get_distance_to_storm(lat, lon, alt, storm)
        if d < min_dist:
            min_dist = d
        if d < storm["radius_km"]:
            active_threat = storm["name"]
            
    return min_dist, active_threat
