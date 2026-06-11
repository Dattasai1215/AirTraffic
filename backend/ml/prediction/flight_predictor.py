import os
import pickle
import numpy as np
import pandas as pd
from pathlib import Path

# Resolve root directory (4 levels up from this file)
# backend/ml/prediction/flight_predictor.py -> root
BASE_DIR = str(Path(__file__).parents[3])
MODEL_DIR = os.path.join(BASE_DIR, "models")

# Load models
lat_model = pickle.load(open(os.path.join(MODEL_DIR, "lat_regressor.pkl"), "rb"))
lon_model = pickle.load(open(os.path.join(MODEL_DIR, "lon_regressor.pkl"), "rb"))
alt_model = pickle.load(open(os.path.join(MODEL_DIR, "alt_regressor.pkl"), "rb"))

def predict_future_position(flight, storm_dist):
    """
    Predicts the coordinates of the aircraft 30 seconds into the future
    using the trained XGBoost regressors.
    """
    # Create input DataFrame
    X = pd.DataFrame([{
        "velocity": flight["velocity"],
        "heading": flight["heading"],
        "vertical_rate": flight["vertical_rate"],
        "altitude": flight["altitude"],
        "storm_dist": storm_dist
    }])
    
    # Predict increments
    delta_lat = float(lat_model.predict(X)[0])
    delta_lon = float(lon_model.predict(X)[0])
    delta_alt = float(alt_model.predict(X)[0])
    
    # Calculate predicted position
    pred_lat = flight["latitude"] + delta_lat
    pred_lon = flight["longitude"] + delta_lon
    pred_alt = np.clip(flight["altitude"] + delta_alt, 100, 13000)
    
    return pred_lat, pred_lon, pred_alt
