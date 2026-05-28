import os
import pickle
import pandas as pd

# Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "anomaly_detector.pkl")

# Load Isolation Forest anomaly detector
anomaly_model = pickle.load(open(MODEL_PATH, "rb"))

def detect_anomaly(flight, heading_rate=0.0):
    """
    Checks flight telemetry for abnormal behavior using the Isolation Forest model.
    Returns:
        is_anomaly (bool): True if flagged as anomalous, False otherwise.
        anomaly_score (float): Anomaly score from the model.
    """
    try:
        squawk_val = float(flight.get("squawk", 1200))
    except ValueError:
        squawk_val = 1200.0
        
    X = pd.DataFrame([{
        "velocity": flight["velocity"],
        "vertical_rate": flight["vertical_rate"],
        "altitude": flight["altitude"],
        "heading_rate": heading_rate,
        "squawk": squawk_val
    }])
    
    # Isolation Forest predicts -1 for anomalies and 1 for inliers
    prediction = anomaly_model.predict(X)[0]
    
    # We can also compute decision function score (lower values are more anomalous)
    score = float(anomaly_model.decision_function(X)[0])
    
    is_anomaly = (prediction == -1)
    
    return is_anomaly, score
