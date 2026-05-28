import numpy as np
import pandas as pd
import os

# Set random seed for reproducibility
np.random.seed(42)

# Ensure directory exists
os.makedirs("data", exist_ok=True)

# 1. Generate Flight Trajectory Data (for predicting 30s future position increments)
# Inputs: velocity (m/s), heading (deg), vertical_rate (m/s), altitude (m), storm_dist (km)
# Outputs: delta_lat (deg), delta_lon (deg), delta_alt (m)
num_trajectory_samples = 15000
velocity = np.random.uniform(100, 280, num_trajectory_samples)  # m/s (approx 200-550 knots)
heading = np.random.uniform(0, 360, num_trajectory_samples)     # degrees
vertical_rate = np.random.uniform(-15, 15, num_trajectory_samples)  # m/s
altitude = np.random.uniform(1500, 11500, num_trajectory_samples)  # meters (5000-38000 ft)
storm_dist = np.random.uniform(0, 100, num_trajectory_samples)  # km

# Base coordinates for simulation (centered around JFK: lat 40.64, lon -73.78)
lat = 40.64
dt = 30.0 # 30 seconds prediction window

# Calculate physics-based increments with some simulated turbulence/wind drift
# 1 degree lat is ~111,000 meters.
# 1 degree lon is ~111,000 * cos(lat) meters.
rad_heading = np.radians(heading)
delta_lat = (velocity * np.cos(rad_heading) * dt) / 111000.0 + np.random.normal(0, 0.0002, num_trajectory_samples)
delta_lon = (velocity * np.sin(rad_heading) * dt) / (111000.0 * np.cos(np.radians(lat))) + np.random.normal(0, 0.0002, num_trajectory_samples)
delta_alt = vertical_rate * dt + np.random.normal(0, 10.0, num_trajectory_samples)

# If close to storm, add more turbulence/drift
storm_effect = storm_dist < 15
delta_lat[storm_effect] += np.random.normal(0, 0.0008, np.sum(storm_effect))
delta_lon[storm_effect] += np.random.normal(0, 0.0008, np.sum(storm_effect))
delta_alt[storm_effect] += np.random.normal(0, 30.0, np.sum(storm_effect))

trajectory_df = pd.DataFrame({
    "velocity": velocity,
    "heading": heading,
    "vertical_rate": vertical_rate,
    "altitude": altitude,
    "storm_dist": storm_dist,
    "delta_lat": delta_lat,
    "delta_lon": delta_lon,
    "delta_alt": delta_alt
})
trajectory_df.to_csv("data/flight_trajectory_data.csv", index=False)
print("Generated data/flight_trajectory_data.csv")


# 2. Generate Aircraft Conflict/Collision Data (for predicting collision probability)
# Features: distance_horizontal (km), distance_vertical (m), relative_velocity (m/s), heading_diff (deg), storm_dist (km)
# Target: conflict (0 or 1)
num_conflict_samples = 20000
dist_h = np.random.exponential(scale=12.0, size=num_conflict_samples) + 0.1 # skewed towards close approaches
dist_v = np.random.exponential(scale=800.0, size=num_conflict_samples) + 10.0
rel_vel = np.random.uniform(10, 450, num_conflict_samples) # relative velocity in m/s
heading_diff = np.random.uniform(0, 180, num_conflict_samples)
storm_dist_c = np.random.uniform(0, 100, num_conflict_samples)

# Air traffic safety separation standards:
# Horizontal separation: 5 nautical miles (~9.26 km)
# Vertical separation: 1000 ft (~304.8 meters)
# Let's say conflict occurs if they violate safety margins, or if they are close and heading towards each other
base_conflict = (dist_h < 8.0) & (dist_v < 350.0)
# Dynamic risk: high relative velocity or converging courses in moderate proximity or turbulent weather
dynamic_risk = (dist_h < 15.0) & (dist_v < 500.0) & (rel_vel > 300.0) & (heading_diff > 90.0)
weather_risk = (dist_h < 10.0) & (dist_v < 400.0) & (storm_dist_c < 15.0)

conflict_prob = 0.05 + 0.85 * (base_conflict | dynamic_risk | weather_risk)
# Clamp probability
conflict_prob = np.clip(conflict_prob, 0.0, 1.0)
conflict = np.random.binomial(1, conflict_prob)

conflict_df = pd.DataFrame({
    "distance_horizontal": dist_h,
    "distance_vertical": dist_v,
    "relative_velocity": rel_vel,
    "heading_diff": heading_diff,
    "storm_dist": storm_dist_c,
    "conflict": conflict
})
conflict_df.to_csv("data/aircraft_conflict_data.csv", index=False)
print("Generated data/aircraft_conflict_data.csv")


# 3. Generate Anomaly Detection Data
# Features: velocity (m/s), vertical_rate (m/s), altitude (m), heading_rate (deg/s), squawk
num_anomaly_samples = 10000
# Normal data
vel_n = np.random.normal(200, 30, num_anomaly_samples)
vr_n = np.random.normal(0, 4, num_anomaly_samples)
alt_n = np.random.uniform(2000, 11000, num_anomaly_samples)
hr_n = np.random.exponential(scale=0.5, size=num_anomaly_samples)
# Standard squawk codes (1200 or 2000 for standard VFR/IFR)
squawk_n = np.random.choice([1200, 2000, 4321, 5678], size=num_anomaly_samples, p=[0.7, 0.2, 0.05, 0.05])

# Add 2% anomalies manually
num_anomalies = int(num_anomaly_samples * 0.02)
anomaly_indices = np.random.choice(num_anomaly_samples, num_anomalies, replace=False)

for idx in anomaly_indices:
    anomaly_type = np.random.choice(["overspeed", "extreme_climb", "emergency_squawk", "erratic"])
    if anomaly_type == "overspeed":
        vel_n[idx] = np.random.uniform(420, 550) # Jet speed limit exceeded significantly
    elif anomaly_type == "extreme_climb":
        vr_n[idx] = np.random.choice([np.random.uniform(45, 60), np.random.uniform(-70, -50)]) # Extreme dive/climb
    elif anomaly_type == "emergency_squawk":
        # Emergency squawk codes: 7500 (hijack), 7600 (radio fail), 7700 (emergency)
        squawk_n[idx] = np.random.choice([7500, 7600, 7700])
        vel_n[idx] = np.random.uniform(120, 220)
    elif anomaly_type == "erratic":
        hr_n[idx] = np.random.uniform(12.0, 25.0) # Spinning or erratic turns
        alt_n[idx] = np.random.uniform(100, 800) # Extremely low altitude flying erratically

anomaly_df = pd.DataFrame({
    "velocity": vel_n,
    "vertical_rate": vr_n,
    "altitude": alt_n,
    "heading_rate": hr_n,
    "squawk": squawk_n
})
anomaly_df.to_csv("data/anomaly_detection_data.csv", index=False)
print("Generated data/anomaly_detection_data.csv")
print("All datasets generated successfully!")
