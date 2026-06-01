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

### Step 3B: Launch the Live Tracking Frontend (Optional but Recommended)

Modern React + Leaflet frontend for production-ready live aircraft tracking. Perfect for public viewing and worldwide deployment.

- **Location:** `frontend/`
- **Runs:** `npm run dev` (development) or deploy to Vercel for production
- **Features:**
  - 🌍 Real-time interactive map with Leaflet
  - ✈️ Live aircraft markers with heading rotation
  - 🔍 Search and filter flights
  - 📊 Live metrics and statistics
  - 🚀 Deploy to Vercel with one click

---

## Technologies Used

### Backend
- **Programming Language**: Python 3.x
- **Machine Learning**: XGBoost, Scikit-learn
- **Data Engineering**: Pandas, NumPy
- **API Fetching**: OpenSky Network API (with custom high-fidelity stateful mock simulation)
- **Visualization**: Streamlit, Plotly 3D
- **Deployment**: Streamlit Cloud

### Frontend (Optional)
- **Framework**: React 18, Vite
- **Mapping**: Leaflet.js
- **Styling**: Tailwind CSS
- **APIs**: OpenSky Network API
- **Deployment**: Vercel

---

## Quick Start

### Backend Setup (Python)

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

### Frontend Setup (React)

For a modern, production-ready interface:

1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Open [http://localhost:5173](http://localhost:5173) in your browser.

### Backend API Server

The backend provides live flight tracking, ML prediction, conflict risk scoring, anomaly detection, and optional AI summary generation.

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the backend server:
   ```bash
   python backend/server.py
   ```
3. Configure the frontend to consume the backend by setting `VITE_API_BASE_URL` to `http://localhost:8000`.

If you want AI summaries, set `OPENAI_API_KEY` before starting the backend:

```bash
set OPENAI_API_KEY=your_api_key
python backend/server.py
```

### Deploy Frontend to GitHub Pages

The repository includes a GitHub Actions workflow that builds the frontend and deploys it to GitHub Pages on every push to `main`.

1. Push your code to the GitHub repository.
2. Ensure GitHub Pages is enabled for the repository and set to use the `gh-pages` branch.
3. The workflow at `.github/workflows/deploy-frontend.yml` will publish `frontend/dist` automatically.

### Recommended Deployment

- Frontend: GitHub Pages or Vercel
- Backend: Render, Railway, Fly.io, or another Python host

For the best experience, run the frontend and backend together locally and point the frontend at `http://localhost:8000`.
