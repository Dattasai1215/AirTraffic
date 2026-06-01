# 🌍 AeroShield Live Tracking Frontend

Modern React + Leaflet real-time aircraft tracking system connected to your Python backend.

## 📦 Features

✨ **Real-time Flight Tracking**
- Live aircraft positions from OpenSky Network API
- Auto-refresh every 10 seconds
- Smooth map interactions with Leaflet

🎯 **Interactive Map**
- Dark-themed radar display
- Click aircraft for detailed telemetry
- Heading-based rotation indicators
- Altitude/Speed/Route visualization

🔍 **Search & Filter**
- Filter by callsign, ICAO code, or country
- Quick aircraft lookup
- Active fleet statistics

⚙️ **System Integration**
- Backend connection for ML predictions (collision detection, anomaly detection)
- Real-time conflict alerts
- Weather-aware flight tracking

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The app will run on **http://localhost:5173**

### 3. Build for Production

```bash
npm run build
```

Output will be in `dist/` folder.

## 🛠️ Tech Stack

- **React 18** - UI framework
- **Vite** - Lightning-fast build tool
- **Leaflet** - Interactive maps
- **Tailwind CSS** - Utility-first styling
- **OpenSky Network API** - Free live flight data

## 🌐 Deployment to Vercel

### 1. Push to GitHub

```bash
git add .
git commit -m "Add live tracking frontend"
git push origin main
```

### 2. Deploy to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click **Import Project**
3. Select your GitHub repo
4. Set:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Click **Deploy**

### 3. Connect Backend (Optional)

If running backend on same server, add environment variable:

```
VITE_API_BASE_URL=https://your-backend.example.com
VITE_BASE_PATH=/
```

## 📡 API Configuration

### Change Tracking Region

Edit `src/App.jsx`:

```javascript
// Change these coordinates to your preferred region
const response = await fetch(
  'https://opensky-network.org/api/states/all?lamin=39.5&lamax=41.5&lomin=-75.0&lomax=-72.0'
);
```

**Common Regions:**
- New York: `?lamin=39.5&lamax=41.5&lomin=-75.0&lomax=-72.0`
- London: `?lamin=51.2&lamax=51.8&lomin=-0.5&lomax=0.3`
- Tokyo: `?lamin=34.5&lamax=35.5&lomin=139.2&lomax=140.2`

### Refresh Rate

Change update interval in `src/App.jsx`:

```javascript
// Refresh every 10 seconds (10000ms)
const interval = setInterval(fetchFlights, 10000)
```

## 🔗 Backend Integration

### Connect to Streamlit Dashboard

Your Streamlit backend (`dashboard/app.py`) runs on port **8501**.

To integrate predictions:

```javascript
// Add in src/App.jsx
const getMLPredictions = async (flight) => {
  const response = await fetch('http://localhost:8501/api/predict', {
    method: 'POST',
    body: JSON.stringify(flight)
  })
  return response.json()
}
```

## 📊 Environment Variables

Create `.env.local`:

```
VITE_OPENSKY_URL=https://opensky-network.org/api/states/all
VITE_API_BASE_URL=http://localhost:8000
VITE_BASE_PATH=/
VITE_REFRESH_INTERVAL=10000
```

## 🧪 Testing

Run in development:

```bash
npm run dev
```

Open developer console (F12) to see API calls and flight data.

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── LiveMap.jsx       # Leaflet map with aircraft markers
│   │   ├── FlightPanel.jsx   # Flight details panel
│   │   ├── SearchBar.jsx     # Search & filter
│   │   └── MetricsBar.jsx    # Stats display
│   ├── App.jsx               # Main app
│   ├── main.jsx              # React entry point
│   └── index.css             # Tailwind styles
├── index.html                # HTML entry point
├── vite.config.js            # Vite configuration
├── tailwind.config.js        # Tailwind theming
└── package.json              # Dependencies
```

## 🎨 Customization

### Theme Colors

Edit `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      dark: {
        900: '#020617',  // Background
        700: '#0f172a',  // Cards
      }
    }
  }
}
```

### Map Tile Provider

Change in `src/components/LiveMap.jsx`:

```javascript
// Use light theme instead of dark
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png')
```

## 🐛 Troubleshooting

**Map not loading?**
- Check browser console for errors
- Ensure Leaflet CSS is loaded
- Try hard refresh (Ctrl+Shift+R)

**No flights showing?**
- Verify OpenSky API is accessible
- Check browser Network tab
- Change tracking region to high-traffic area

**Slow performance?**
- Reduce refresh interval
- Filter flights by region
- Use browser DevTools to profile

## 📚 Resources

- [React Documentation](https://react.dev)
- [Leaflet Documentation](https://leafletjs.com)
- [Tailwind CSS](https://tailwindcss.com)
- [OpenSky Network API](https://opensky-network.org/apidoc/index.html)
- [Vite Documentation](https://vitejs.dev)

## 📝 License

Part of AeroShield project. MIT License.

## 🚀 Next Steps

1. Run the frontend: `npm run dev`
2. Keep Streamlit backend running: `streamlit run dashboard/app.py`
3. Deploy frontend to Vercel
4. Share URL with colleagues for live viewing!
