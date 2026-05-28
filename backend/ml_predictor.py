import pickle
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "collision_model.pkl")

model = pickle.load(open(MODEL_PATH, "rb"))

def predict_collision(dist, vel, alt):

    X = np.array([[dist, vel, alt]])

    prob = model.predict_proba(X)[0][1]

    return prob