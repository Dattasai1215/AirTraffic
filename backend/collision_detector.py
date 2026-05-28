import os
import pickle
import numpy as np
import pandas as pd

# Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "conflict_classifier.pkl")

# Load model
conflict_model = pickle.load(open(MODEL_PATH, "rb"))

def calculate_separation(f1, f2):
    """
    Calculates the 3D spatial separation between two flights.
    Returns:
        dist_h (float): Horizontal distance in km
        dist_v (float): Vertical separation in meters
    """
    lat1, lon1, alt1 = f1["latitude"], f1["longitude"], f1["altitude"]
    lat2, lon2, alt2 = f2["latitude"], f2["longitude"], f2["altitude"]
    
    # Horizontal distance in km (using Haversine-like flat approximation for small regions)
    dx = (lat1 - lat2) * 111.0
    dy = (lon1 - lon2) * 111.0 * np.cos(np.radians((lat1 + lat2) / 2.0))
    dist_h = np.sqrt(dx**2 + dy**2)
    
    # Vertical distance in meters
    dist_v = abs(alt1 - alt2)
    
    return dist_h, dist_v

def predict_collision_risk(f1, f2, dist_h, dist_v, storm_dist):
    """
    Uses the trained XGBoost Classifier to predict the conflict probability.
    """
    # Calculate relative velocity vector magnitude (m/s)
    h1_rad = np.radians(f1["heading"])
    h2_rad = np.radians(f2["heading"])
    
    vx1 = f1["velocity"] * np.cos(h1_rad)
    vy1 = f1["velocity"] * np.sin(h1_rad)
    vz1 = f1["vertical_rate"]
    
    vx2 = f2["velocity"] * np.cos(h2_rad)
    vy2 = f2["velocity"] * np.sin(h2_rad)
    vz2 = f2["vertical_rate"]
    
    rel_vx = vx1 - vx2
    rel_vy = vy1 - vy2
    rel_vz = vz1 - vz2
    
    rel_vel = np.sqrt(rel_vx**2 + rel_vy**2 + rel_vz**2)
    
    # Calculate heading difference (0 to 180 degrees)
    heading_diff = abs(f1["heading"] - f2["heading"])
    if heading_diff > 180.0:
        heading_diff = 360.0 - heading_diff
        
    X = pd.DataFrame([{
        "distance_horizontal": dist_h,
        "distance_vertical": dist_v,
        "relative_velocity": rel_vel,
        "heading_diff": heading_diff,
        "storm_dist": storm_dist
    }])
    
    prob = float(conflict_model.predict_proba(X)[0][1])
    return prob