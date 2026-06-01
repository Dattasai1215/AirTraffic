# 🚀 Deployment Guide - AeroShield

Complete guide to deploy AeroShield to production with real-time flight tracking, ML predictions, and AI summaries.

## Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Docker Setup](#docker-setup)
3. [Deploy to Render](#deploy-to-render)
4. [Deploy to Railway](#deploy-to-railway)
5. [Deploy Frontend to Vercel/GitHub Pages](#deploy-frontend-to-vercelgithub-pages)
6. [Environment Variables](#environment-variables)
7. [Monitoring & Logs](#monitoring--logs)

---

## Local Development Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- Git

### Step 1: Clone and Install

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/AirTraffic.git
cd AirTraffic

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### Step 2: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env.local

# .env.local content:
# HOST=127.0.0.1
# PORT=8000
# VITE_API_BASE_URL=http://localhost:8000
```

### Step 3: Generate ML Models (First Time Only)

```bash
# Generate flight datasets
python data/generate_flight_data.py

# Train XGBoost and Isolation Forest models
python models/train_xgboost_models.py
```

### Step 4: Run Backend and Frontend

In separate terminals:

```bash
# Terminal 1: Start Backend API
python backend/server.py
# Backend will be available at http://localhost:8000

# Terminal 2: Start Frontend
cd frontend
npm run dev
# Frontend will be available at http://localhost:5173
```

Visit: **http://localhost:5173**

---

## Docker Setup

### Run Locally with Docker Compose

```bash
# Build and start both backend and frontend
docker-compose up --build

# Backend: http://localhost:8000
# Frontend: http://localhost:5173
```

### Build Docker Image for Production

```bash
# Build the image
docker build -t aeroshield:latest .

# Run the container
docker run -p 8000:8000 \
  -e FLASK_ENV=production \
  -e OPENAI_API_KEY=your_key_here \
  aeroshield:latest
```

---

## Deploy to Render

### Deploy Backend to Render

1. **Sign up** at [render.com](https://render.com)
2. **Create New > Web Service**
3. **Connect your GitHub repository**
4. **Configure:**
   - **Name**: `aeroshield-backend`
   - **Environment**: `Docker`
   - **Root Directory**: (leave empty)

5. **Set Environment Variables:**
   - `FLASK_ENV` = `production`
   - `OPENAI_API_KEY` = your API key (optional)

6. **Advanced:**
   - Auto-deploy from `main` branch: Yes
   - Health Check Path: `/api/status`

7. **Create Web Service**

Your backend URL will be: `https://aeroshield-backend-xxx.onrender.com`

### Deploy Frontend to Render

1. **Create New > Static Site**
2. **Connect your GitHub repository**
3. **Configure:**
   - **Name**: `aeroshield-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`

4. **Set Environment Variables:**
   - `VITE_API_BASE_URL` = `https://aeroshield-backend-xxx.onrender.com`

5. **Deploy**

---

## Deploy to Railway

### Deploy Backend to Railway

1. **Sign up** at [railway.app](https://railway.app)
2. **New Project > Deploy from GitHub repo**
3. **Select your AirTraffic repository**
4. **Set Environment Variables:**
   - `FLASK_ENV` = `production`
   - `OPENAI_API_KEY` = your API key

5. **Deploy**

### Deploy Frontend to Railway

1. **Create new service > Node.js**
2. **Connect your GitHub repo**
3. **Set start command**: `cd frontend && npm run build && npm run preview`
4. **Environment Variable:**
   - `VITE_API_BASE_URL` = your Railway backend URL

---

## Deploy Frontend to Vercel/GitHub Pages

### GitHub Pages (Automatic via Actions)

GitHub Actions will automatically deploy on push to `main`:

1. **Enable GitHub Pages:**
   - Go to Settings > Pages
   - Source: `Deploy from a branch`
   - Branch: `gh-pages`
   - Folder: `/ (root)`

2. **Push code:**
   ```bash
   git push origin main
   ```

Your site: `https://YOUR_USERNAME.github.io/AirTraffic`

### Vercel (One-Click)

1. Go to [vercel.com/import](https://vercel.com/import)
2. **Import your GitHub repository**
3. **Configure:**
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

4. **Environment Variables:**
   - `VITE_API_BASE_URL` = your backend URL (Render/Railway)

5. **Deploy**

---

## Environment Variables

### Backend (.env / .env.local)

```bash
HOST=0.0.0.0                              # Bind address
PORT=8000                                 # Port number
FLASK_ENV=production                      # or development
OPENAI_API_KEY=sk-your-api-key           # Optional, for AI summaries
```

### Frontend

```bash
VITE_API_BASE_URL=https://your-backend-url.com
```

---

## Monitoring & Logs

### Render

- **Logs**: Dashboard > Service > Logs tab
- **View**: Real-time output

### Railway

- **Logs**: Service > Logs tab  
- **Metrics**: Real-time dashboard

---

## 📁 File Structure

```
AirTraffic/
├── backend/server.py              # Main Flask API
├── frontend/                       # React app
│   ├── dist/                      # Built files
│   ├── src/
│   └── package.json
├── models/                        # ML models (commit these!)
├── Dockerfile                     # Docker build
├── docker-compose.yml
├── Procfile                       # Heroku/Render
├── .env.example
└── requirements.txt
```

---

## Full Deployment URLs (Example)

- **Backend**: `https://aeroshield-backend-xxx.onrender.com`
- **Frontend**: `https://your-username.github.io/AirTraffic`
- **Flights API**: `https://aeroshield-backend-xxx.onrender.com/api/flights`

Happy flying! ✈️

