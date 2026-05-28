# ✈️ AeroShield – AI Air Traffic Collision Prediction System

AI-powered aviation monitoring system that tracks aircraft positions in real time, forecasts future trajectories, detects mid-air conflicts, and flags telemetry anomalies under dynamic weather conditions.

The platform visualizes active airspace in 3D and leverages advanced machine learning to provide decision support to Air Traffic Control (ATC).

## Project Workflow

```
Flight & Anomaly Data Generation
             ↓
  XGBoost & Isolation Forest Training
             ↓
Real-Time Flight Tracking (OpenSky / Mock Fallback)
             ↓
Flight Path Projection (XGBoost Regressor)
             ↓
Conflict Classification (XGBoost Classifier)
             ↓
Flight Telemetry Anomaly Detection (Isolation Forest)
             ↓
3D Airspace Weather-Aware Dashboard Visualization
```

### Step 1: Generate Flight Simulation Dataset

Creates synthetic datasets for flight trajectories, aircraft encounter risks, and telemetry anomalies.

- **Runs:** `python data/generate_flight_data.py`
- **Outputs:**
  - `data/flight_trajectory_data.csv` (time-series)
  - `data/aircraft_conflict_data.csv` (classification)
  - `data/anomaly_detection_data.csv` (anomaly detection)

### Step 2: Train the Machine Learning Models

Trains the XGBoost regressors (latitude, longitude, altitude future offsets), XGBoost classifier (collision risk), and Isolation Forest (flight anomaly detector).

- **Runs:** `python models/train_xgboost_models.py`
- **Outputs:**
  - `models/lat_regressor.pkl`
  - `models/lon_regressor.pkl`
  - `models/alt_regressor.pkl`
  - `models/conflict_classifier.pkl`
  - `models/anomaly_detector.pkl`

### Step 3: Launch the Airspace Dashboard

Runs the Streamlit dashboard providing a live, 3D weather-aware radar screen, dropdown aircraft telemetry inspector, and ATC console logs.

- **Runs:** `streamlit run dashboard/app.py`

---

## Technologies Used

- **Programming Language**: Python
- **Machine Learning**: XGBoost, Scikit-learn
- **Data Engineering**: Pandas, NumPy
- **API Fetching**: OpenSky API (with custom high-fidelity stateful mock simulation)
- **Visualization**: Streamlit, Plotly 3D

---

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Generate flight datasets:
   ```bash
   python data/generate_flight_data.py
   ```
3. Train XGBoost and Isolation Forest models:
   ```bash
   python models/train_xgboost_models.py
   ```
4. Start the ATC monitoring room:
   ```bash
   streamlit run dashboard/app.py
   ```
5. Open [http://localhost:8501](http://localhost:8501) in your browser.
