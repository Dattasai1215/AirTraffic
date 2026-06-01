# ⚡ Quick Start Guide - AeroShield

Get AeroShield running in **5-10 minutes** with production-ready tracking.

---

## 🚀 Start Here (3 Options)

### Option A: Lite Version (No Backend)
**Best for:** Quick testing, learning, minimal setup

```bash
git clone https://github.com/YOUR_USERNAME/AirTraffic.git
cd AirTraffic/frontend
npm install
npm run dev
```

Open: **http://localhost:5173**

✅ Works immediately | Uses free OpenSky API | No models needed

---

### Option B: Full Stack (Recommended)
**Best for:** Development, ML features, AI summaries

#### 1. Clone & Setup Backend

```bash
git clone https://github.com/YOUR_USERNAME/AirTraffic.git
cd AirTraffic

# Create and activate Python environment
python -m venv venv
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Start backend
python backend/server.py
# Backend at http://localhost:8000
```

#### 2. Start Frontend (New Terminal)

```bash
cd AirTraffic/frontend
npm install
npm run dev
# Frontend at http://localhost:5173
```

Open: **http://localhost:5173**

✅ ML predictions | AI summaries | Collision detection | Anomalies

---

### Option C: Docker (All-in-One)
**Best for:** Fastest setup, no dependency issues

```bash
git clone https://github.com/YOUR_USERNAME/AirTraffic.git
cd AirTraffic
docker-compose up --build
```

Open: **http://localhost:5173**

Backend: **http://localhost:8000**

✅ No installation needed | Fully isolated | Production-ready

---

## ✨ What You Get

| Feature | Lite | Full | Docker |
|---------|------|------|--------|
| 🛫 Live Flights | ✅ | ✅ | ✅ |
| 🤖 ML Predictions | ❌ | ✅ | ✅ |
| ⚠️ Collision Alerts | ❌ | ✅ | ✅ |
| 🔍 Anomaly Detection | ❌ | ✅ | ✅ |
| 🧠 AI Summaries | ❌ | ✅* | ✅* |
| 📊 Real-time Map | ✅ | ✅ | ✅ |

*Requires OpenAI key in `.env`

---

## 🔧 Configuration (Optional)

### Add OpenAI API Key (For AI Summaries)

1. Get your key from [platform.openai.com](https://platform.openai.com)
2. Create `.env` file in project root:

```bash
OPENAI_API_KEY=sk-your-key-here
PORT=8000
FLASK_ENV=development
VITE_API_BASE_URL=http://localhost:8000
```

3. Restart backend:
```bash
python backend/server.py
```

Now the app will generate AI summaries of flight status! 🧠

---

## 🌐 Deploy Live (Choose One)

### Deploy to Render (Easiest)

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Select your repo, set to Docker
4. Deploy ✅

### Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Select repo, auto-deploys on push ✅

### Deploy Frontend to GitHub Pages

1. Push to `main` branch
2. GitHub Actions auto-deploys
3. Live at: `https://YOUR_USERNAME.github.io/AirTraffic` ✅

See [DEPLOYMENT.md](DEPLOYMENT.md) for full deployment guide.

---

## 🆘 Troubleshooting

### "No flights showing"
- Check OpenSky API status
- Try different region coordinates
- Verify internet connection

### "Backend connection error"
- Ensure backend is running: `python backend/server.py`
- Check `VITE_API_BASE_URL` is correct
- Verify ports 8000 and 5173 are free

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
pip install flask flask-cors openai
python backend/server.py
```

### "Port already in use"
```bash
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -i :8000
kill -9 <PID>
```

---

## 📖 Next Steps

1. ✅ Run locally (choose Option A, B, or C above)
2. 📖 Read [README.md](README.md) for full features
3. 🚀 Deploy with [DEPLOYMENT.md](DEPLOYMENT.md)
4. 🎨 Customize map region, colors
5. 🔌 Add to your own project

---

## 💡 Pro Tips

**Change Tracked Region:**
Edit frontend `App.jsx` - Look for OpenSky URL with coordinates:
```
lamin=39.5&lamax=41.5&lomin=-75.0&lomax=-72.0
```

Popular regions:
- **London**: `51.2, 51.8, -0.5, 0.3`
- **Tokyo**: `34.5, 35.5, 139.2, 140.2`
- **Dubai**: `24.8, 25.3, 54.8, 55.5`

---

## 🎉 Ready?

```bash
# Pick one and go:

# Lite
cd frontend && npm install && npm run dev

# Full Stack
python backend/server.py  # Terminal 1
cd frontend && npm run dev  # Terminal 2

# Docker
docker-compose up --build
```

**Your live flight tracker is running!** ✈️

Visit http://localhost:5173 and start tracking! 🌍


## 🌍 Deploy to Production

### Frontend (React) → Vercel (1 click)

```bash
cd frontend
npm run build  # Creates dist/

# Then push to GitHub and deploy via vercel.com
```

### Backend (Streamlit) → Streamlit Cloud

Go to [share.streamlit.io](https://share.streamlit.io)

---

## 📍 Track Different Regions

Edit `frontend/src/App.jsx`:

```javascript
// Line ~50 - Change coordinates
const response = await fetch(
  'https://opensky-network.org/api/states/all?lamin=39.5&lamax=41.5&lomin=-75.0&lomax=-72.0'
);
```

**Presets:**
- **New York:** `lamin=39.5&lamax=41.5&lomin=-75.0&lomax=-72.0`
- **London:** `lamin=51.2&lamax=51.8&lomin=-0.5&lomax=0.3`
- **Tokyo:** `lamin=34.5&lamax=35.5&lomin=139.2&lomax=140.2`

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| npm not found | Install Node.js: https://nodejs.org |
| Port 5173 in use | Change in `frontend/vite.config.js` |
| No flights showing | Change region to high-traffic area |
| Build fails | Run `npm install` again in frontend/ |

---

## 🚀 You're Ready!

Your live flight tracking system is complete. Choose your setup above and start tracking! 🎉
