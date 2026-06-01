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

### Step 3: Launch Backend API

Runs the Flask backend providing real-time flight tracking, ML predictions, collision/anomaly detection, and optional AI summaries.

- **Runs:** `python backend/server.py`
- **Features:**
  - 🔌 REST API endpoints
  - 🤖 ML inference in real-time
  - 🌪️ Weather-aware predictions
  - 🧠 Optional OpenAI summaries
  - 📊 CORS-enabled for frontend

### Step 4: Launch the Live Tracking Frontend

Modern React + Leaflet frontend for production-ready live aircraft tracking. Perfect for public viewing and worldwide deployment.

- **Location:** `frontend/`
- **Runs:** `npm run dev` (development) or `npm run build` (production)
- **Features:**
  - 🌍 Real-time interactive map with Leaflet
  - ✈️ Live aircraft markers with heading rotation
  - 🔍 Search and filter flights
  - 📊 Live metrics and statistics
  - 🚀 Easy deployment to GitHub Pages/Vercel

---

## Technologies Used

### Backend
- **Language**: Python 3.x
- **Framework**: Flask
- **ML**: XGBoost, Scikit-learn, Isolation Forest
- **Data**: Pandas, NumPy
- **API**: OpenSky Network API
- **Deployment**: Docker, Render, Railway
- **Optional AI**: OpenAI GPT-3.5

### Frontend
- **Framework**: React 18 + Vite
- **Mapping**: Leaflet.js
- **Styling**: Tailwind CSS
- **HTTP**: Axios
- **Deployment**: GitHub Pages, Vercel, Render

---

## Quick Start

### Option 1: Frontend Only (Direct OpenSky Data)

```bash
cd frontend
npm install
npm run dev
# Open http://localhost:5173
```

**No backend needed. Uses free OpenSky API directly.**

### Option 2: Full Stack (Recommended)

In **Terminal 1** - Start Backend:
```bash
python -m venv venv
# Activate: venv\Scripts\activate (Windows) or source venv/bin/activate (Mac/Linux)
pip install -r requirements.txt
python backend/server.py
# Backend at http://localhost:8000
```

In **Terminal 2** - Start Frontend:
```bash
cd frontend
npm install
npm run dev
# Frontend at http://localhost:5173
```

**Features:** ML predictions, AI summaries, anomaly detection, collision detection

### Option 3: Docker (All-in-One)

```bash
docker-compose up --build
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
```

### Option 4: Generate Models First (One-Time)

```bash
python data/generate_flight_data.py
python models/train_xgboost_models.py
```

*These create ML models in `/models/`. Commit them to GitHub.*

---

## Backend API Endpoints

Once the backend is running at `http://localhost:8000`:

### Get Live Flights + ML Predictions

```bash
curl http://localhost:8000/api/flights
```

**Response:**
- **flights[]**: Array of aircraft with position, speed, heading
- **conflictCount**: Number of detected conflicts
- **summary**: AI-generated briefing
- **alerts[]**: Active anomalies and warnings
- **weather_zones[]**: Storm/turbulence areas

### Check Backend Status

```bash
curl http://localhost:8000/api/status
```

---

## Backend Setup (Python)

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Generate flight datasets (first time only):
   ```bash
   python data/generate_flight_data.py
   ```
3. Train ML models (first time only):
   ```bash
   python models/train_xgboost_models.py
   ```
4. Start the backend:
   ```bash
   python backend/server.py
   ```
   Backend at `http://localhost:8000`

### Configure Environment (Optional)

Copy `.env.example` to `.env.local`:

```bash
HOST=127.0.0.1
PORT=8000
FLASK_ENV=development
FLASK_DEBUG=1
OPENAI_API_KEY=sk-your-key  # Optional, for AI summaries
VITE_API_BASE_URL=http://localhost:8000
```

---

## Frontend Setup (React)

## Frontend Setup (React)

1. Navigate to frontend folder:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start development server:
   ```bash
   npm run dev
   ```
   Frontend at `http://localhost:5173`

4. Build for production:
   ```bash
   npm run build
   # Output: frontend/dist/
   ```

---

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide covering:

- **Local Docker Setup** with `docker-compose`
- **Deploy to Render** (backend + frontend)
- **Deploy to Railway** (backend + frontend)
- **Deploy to GitHub Pages** (frontend via Actions)
- **Deploy to Vercel** (frontend)
- **Environment Variables** configuration
- **Monitoring & Logs**

### Quick Deploy to Render (5 minutes)

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. **New Web Service**:
   - Select your AirTraffic repo
   - Root Directory: (empty)
   - Environment: Docker
   - Set `FLASK_ENV=production` and `OPENAI_API_KEY` (optional)
4. **New Static Site**:
   - Root Directory: `frontend`
   - Build: `npm install && npm run build`
   - Publish: `dist`
   - Set `VITE_API_BASE_URL` to your Render backend URL

Your site is now live! ✈️
