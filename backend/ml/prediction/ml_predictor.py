import pickle
import os
import numpy as np
from pathlib import Path

# Resolve root directory (4 levels up from this file)
# backend/ml/prediction/ml_predictor.py -> root
BASE_DIR = str(Path(__file__).parents[3])
MODEL_PATH = os.path.join(BASE_DIR, "models", "collision_model.pkl")

model = pickle.load(open(MODEL_PATH, "rb"))

def predict_collision(dist, vel, alt):

    X = np.array([[dist, vel, alt]])

    prob = model.predict_proba(X)[0][1]

    return prob
