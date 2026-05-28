## 🎯 Quick Start: Run Your Live Flight Tracking System

### Option 1: Streamlit Only (Fastest)

```bash
# Already running on port 8501
streamlit run dashboard/app.py
```

👉 Open: http://localhost:8501

---

### Option 2: React Frontend (Modern UI) ⭐ RECOMMENDED

```bash
cd frontend
npm install
npm run dev
```

👉 Open: http://localhost:5173

**Features:**
- 🌍 Live map with real aircraft
- ✈️ Click aircraft for details
- 🔍 Search by callsign/country
- 📊 Real-time stats
- 🚀 Easy Vercel deployment

---

### Option 3: Both Running Together (Full Stack)

**Terminal 1 - Backend:**
```bash
streamlit run dashboard/app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8501

---

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
