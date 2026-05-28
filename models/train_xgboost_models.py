import pandas as pd
import numpy as np
import pickle
import os
import xgboost as xgb
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error

# Ensure directory exists
os.makedirs("models", exist_ok=True)

print("--- Training Flight Path Regressor (XGBoost) ---")
traj_data = pd.read_csv("data/flight_trajectory_data.csv")
X_traj = traj_data[["velocity", "heading", "vertical_rate", "altitude", "storm_dist"]]
y_lat = traj_data["delta_lat"]
y_lon = traj_data["delta_lon"]
y_alt = traj_data["delta_alt"]

# Split data
X_train_t, X_test_t, y_train_lat, y_test_lat = train_test_split(X_traj, y_lat, test_size=0.2, random_state=42)
_, _, y_train_lon, y_test_lon = train_test_split(X_traj, y_lon, test_size=0.2, random_state=42)
_, _, y_train_alt, y_test_alt = train_test_split(X_traj, y_alt, test_size=0.2, random_state=42)

# Train XGBoost regressors
lat_model = xgb.XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
lat_model.fit(X_train_t, y_train_lat)
lat_rmse = np.sqrt(mean_squared_error(y_test_lat, lat_model.predict(X_test_t)))
print(f"Latitude Regressor RMSE: {lat_rmse:.6f}")

lon_model = xgb.XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
lon_model.fit(X_train_t, y_train_lon)
lon_rmse = np.sqrt(mean_squared_error(y_test_lon, lon_model.predict(X_test_t)))
print(f"Longitude Regressor RMSE: {lon_rmse:.6f}")

alt_model = xgb.XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
alt_model.fit(X_train_t, y_train_alt)
alt_rmse = np.sqrt(mean_squared_error(y_test_alt, alt_model.predict(X_test_t)))
print(f"Altitude Regressor RMSE: {alt_rmse:.2f} meters")

pickle.dump(lat_model, open("models/lat_regressor.pkl", "wb"))
pickle.dump(lon_model, open("models/lon_regressor.pkl", "wb"))
pickle.dump(alt_model, open("models/alt_regressor.pkl", "wb"))


print("\n--- Training Collision Risk Classifier (XGBoost) ---")
conflict_data = pd.read_csv("data/aircraft_conflict_data.csv")
X_conf = conflict_data[["distance_horizontal", "distance_vertical", "relative_velocity", "heading_diff", "storm_dist"]]
y_conf = conflict_data["conflict"]

X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_conf, y_conf, test_size=0.2, random_state=42)

conflict_model = xgb.XGBClassifier(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42)
conflict_model.fit(X_train_c, y_train_c)
conf_acc = accuracy_score(y_test_c, conflict_model.predict(X_test_c))
print(f"Conflict Classifier Accuracy: {conf_acc * 100:.2f}%")

pickle.dump(conflict_model, open("models/conflict_classifier.pkl", "wb"))


print("\n--- Training Anomaly Detector (Isolation Forest) ---")
anomaly_data = pd.read_csv("data/anomaly_detection_data.csv")
X_anom = anomaly_data[["velocity", "vertical_rate", "altitude", "heading_rate", "squawk"]]

# We train Isolation Forest on the data (contamination set to ~2.5% to match our simulated anomaly rate)
anomaly_model = IsolationForest(contamination=0.025, random_state=42)
anomaly_model.fit(X_anom)

# Test detection
pred_anom = anomaly_model.predict(X_anom)
num_anomalies_detected = sum(pred_anom == -1)
print(f"Anomalies detected: {num_anomalies_detected} out of {len(X_anom)}")

pickle.dump(anomaly_model, open("models/anomaly_detector.pkl", "wb"))

print("\nAll models trained and saved to models/ directory successfully!")
