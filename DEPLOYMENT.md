# 🚀 AeroShield Deployment Guide

Complete guide to deploy both Streamlit backend and React frontend for live production tracking.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Your AeroShield System               │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  🌍 Frontend (Optional)              🔧 Backend        │
│  React + Leaflet                    Python + ML         │
│  Vercel Deployment                  Streamlit Cloud     │
│                                                           │
│  Live Map      ←→    HTTP APIs  ←→    Predictions     │
│  Tracking      ←→    Real-time  ←→    Anomalies       │
│  Search        ←→    Flights    ←→    Collisions      │
│                │                 │                      │
│                └─────────────────┘                      │
│                   OpenSky API ↓                          │
│              Global Flight Data Stream                   │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Deployment Path 1: Backend Only (Easiest)

### Deploy Streamlit Dashboard to Streamlit Cloud

1. **Create Streamlit Cloud Account**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign up with GitHub

2. **Deploy Dashboard**
   - Click "New App"
   - Select repo: `Dattasai1215/AirTraffic`
   - Select branch: `main`
   - Enter app path: `dashboard/app.py`
   - Click **Deploy**

3. **Access Your Dashboard**
   ```
   https://aeroshield-[your-username].streamlit.app
   ```

✅ **Done!** Your Streamlit dashboard is now live.

---

## 🌍 Deployment Path 2: Full Stack (Recommended)

### A. Deploy Streamlit Backend

Follow **Deployment Path 1** above.

**Note your backend URL:**
```
https://aeroshield-[your-username].streamlit.app
```

### B. Deploy React Frontend to Vercel

#### 1. Setup Frontend for Production

```bash
cd frontend
npm install
npm run build
```

#### 2. Create Vercel Project

```bash
npm install -g vercel
vercel login
vercel
```

Or use **Vercel Web Dashboard**:

1. Go to [vercel.com](https://vercel.com)
2. Click **Import Project**
3. Select your GitHub repository
4. **Configure:**
   - **Framework**: React
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

5. **Environment Variables** (Optional):
   ```
   VITE_BACKEND_URL=https://aeroshield-[your-username].streamlit.app
   VITE_REFRESH_INTERVAL=10000
   ```

6. Click **Deploy**

#### 3. Your Live Site

```
https://your-project-name.vercel.app
```

---

## 🔗 Connecting Frontend to Backend

### Enable Cross-Origin (CORS)

Add to `dashboard/app.py` (Streamlit):

```python
import streamlit as st

st.set_page_config(
    page_title="AeroShield",
    initial_sidebar_state="collapsed"
)

# Enable CORS headers
from streamlit.web.server import Server
if 'server' in dir(st):
    st.set_page_config(
        page_config={'allowOriginOverride': True}
    )
```

### Update Frontend API Calls

Edit `frontend/src/App.jsx`:

```javascript
// Get from environment or default
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 
  'https://aeroshield-[your-username].streamlit.app'

// Fetch predictions from backend
const getMLPredictions = async (flight) => {
  try {
    const response = await fetch(`${BACKEND_URL}/api/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(flight),
      mode: 'cors'
    })
    return response.json()
  } catch (error) {
    console.error('Backend unavailable, showing frontend-only data')
    return null
  }
}
```

---

## 📊 Hybrid Deployment Setup (Best Practice)

### Architecture

```
Client Browser
    ↓
Frontend: Vercel
├─ Real-time map
├─ Live OpenSky data
└─ Search/filter UI
    ↓ (optional ML calls)
Backend: Streamlit Cloud
├─ Collision prediction
├─ Anomaly detection
└─ Weather analysis
```

### Data Flow

1. **Frontend** fetches live flights from **OpenSky API** (free, no auth)
2. **Frontend** optionally calls **Backend** for ML predictions
3. **Backend** uses same OpenSky data + ML models
4. All data displayed in real-time on the map

### Advantages

✅ Frontend is fast and independent (works even if backend is down)
✅ Backend provides intelligence layer (predictions, anomalies)
✅ No single point of failure
✅ Easy to scale separately

---

## 🛠️ Post-Deployment Configuration

### 1. Update Region Tracking

Edit `frontend/src/App.jsx` to track different regions:

```javascript
// Change these coordinates
const REGION = {
  lamin: 39.5,   // Min latitude
  lamax: 41.5,   // Max latitude
  lomin: -75.0,  // Min longitude
  lomax: -72.0   // Max longitude
};
```

**Popular Regions:**
- London: `51.2, 51.8, -0.5, 0.3`
- Tokyo: `34.5, 35.5, 139.2, 140.2`
- Singapore: `1.0, 1.5, 103.5, 104.5`
- Dubai: `24.8, 25.3, 54.8, 55.5`

### 2. Custom Domain (Optional)

**For Vercel Frontend:**

1. Buy domain (Namecheap, GoDaddy, etc.)
2. In Vercel Dashboard → Settings → Domains
3. Add custom domain and follow DNS instructions

**For Streamlit Backend:**

Streamlit Cloud uses their subdomain only. Use a reverse proxy if needed.

### 3. Environment Variables

**Create `frontend/.env.production`:**

```
VITE_BACKEND_URL=https://aeroshield-[your-username].streamlit.app
VITE_REFRESH_INTERVAL=10000
NODE_ENV=production
```

Deploy again on Vercel after updating.

---

## 📈 Monitoring & Maintenance

### Check Deployment Status

**Vercel Frontend:**
```
https://vercel.com → Projects → Select project → Deployments
```

**Streamlit Backend:**
```
https://share.streamlit.io → App settings
```

### Logs

**Vercel:**
```bash
vercel logs --prod
```

**Streamlit:**
- View in console when app is running
- Check Settings → Logs in Streamlit Cloud

### Common Issues

| Issue | Solution |
|-------|----------|
| Frontend shows no flights | Check OpenSky API status or change region |
| Map not loading | Clear browser cache, ensure Leaflet CSS loaded |
| Backend connection fails | Add backend URL to frontend env vars |
| Vercel build failing | Check `frontend/package.json` in root |

---

## 🔒 Security Best Practices

1. **API Keys** - Store in environment variables, never commit
2. **CORS** - Configure properly to avoid exposing backend
3. **Rate Limits** - OpenSky free tier: 4,000 requests/hour
4. **Authentication** - Add if needed for private deployment

---

## 💰 Cost Breakdown

| Service | Free Tier | Cost |
|---------|-----------|------|
| **Vercel** | 100GB bandwidth/mo | $20/mo if exceeded |
| **Streamlit Cloud** | Unlimited | $5-1000/mo (optional pro) |
| **OpenSky API** | 4k req/hr | Free (generous) |
| **Total** | ✅ Free | ~$0-25/mo |

---

## 🎉 Deployment Complete!

Your live tracking system is now accessible worldwide:

- **Frontend:** `https://your-app.vercel.app`
- **Backend:** `https://aeroshield-[user].streamlit.app`
- **Data:** Real-time from OpenSky Network

### Share With Others

```
🌍 Live Flight Tracking: https://your-app.vercel.app
📊 AI Dashboard: https://aeroshield-[user].streamlit.app
```

---

## 📚 Troubleshooting

### Issue: "CORS Error" in Console

**Fix:** Ensure backend is running, add proper headers

### Issue: Map shows only 1-2 flights

**Fix:** Change region to high-traffic area (JFK, LAX, London, etc.)

### Issue: Build fails on Vercel

**Fix:** Ensure `frontend/` has all files, check `package.json`

### Issue: Streamlit app won't start

**Fix:** Run `python models/train_xgboost_models.py` locally first

---

## 🚀 Next Steps

1. ✅ Deploy backend to Streamlit Cloud
2. ✅ Deploy frontend to Vercel
3. 📧 Share URLs with team/public
4. 📊 Monitor in real-time
5. 🎨 Customize colors and regions
6. 🔧 Add more features (alerts, weather layer, etc.)

**Your AeroShield system is live!** ✈️
