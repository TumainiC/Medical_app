# Dashboard Integration Guide

## Overview

Your custom React dashboard from `build-my-dashboard` has been successfully integrated with the Flask backend!

## What Was Done

### 1. **Built the React Dashboard**
- Installed all npm dependencies
- Built the production bundle with `npm run build`
- Generated optimized static files in `dist/` folder

### 2. **Created Backend Integration**
- Copied built files to `static/dashboard/` directory
- Created `templates/dashboard.html` as the integration bridge
- Added `/dashboard` route in Flask app

### 3. **Enhanced React Components**
- Created `IndexBackendIntegrated.tsx` with backend API integration
- Added TypeScript type declarations for window API
- Implemented real-time data updates
- Added loading and error states

### 4. **Backend API Bridge**
- JavaScript bridge in dashboard.html connects React to Flask APIs
- Automatic data fetching on page load
- Auto-refresh every 60 seconds
- Global `window.healthAPI` object for React components

## How It Works

```
┌─────────────────┐
│  Flask Backend  │
│  (Python APIs)  │
└────────┬────────┘
         │
         │ REST APIs
         │
┌────────▼────────┐
│ dashboard.html  │
│  (Integration)  │
└────────┬────────┘
         │
         │ healthAPI
         │
┌────────▼────────┐
│  React Dashboard│
│  (Components)   │
└─────────────────┘
```

## Access the Dashboard

### Start the Flask Server
```bash
python app.py
```

### Visit the Dashboard
- **New React Dashboard**: http://localhost:5000/dashboard
- **Original Dashboard**: http://localhost:5000/

## Available APIs

The React dashboard automatically connects to:

1. **`/api/health/simulate`** - Generate health data
2. **`/api/health/dashboard/:userId`** - Get dashboard data
3. **Auto-refresh** - Updates every 60 seconds

## Backend Integration Features

### ✅ Real-Time Data
- Fetches data from Flask backend on load
- Displays actual health metrics from ML models
- Shows anomaly detection results
- Displays risk assessment levels

### ✅ Dynamic Updates
- Heart Rate from backend
- Blood Oxygen levels
- Temperature readings
- Respiration rate
- Health score
- Statistics (total records, anomalies, averages)

### ✅ Error Handling
- Loading states while fetching data
- Error messages with retry functionality
- Graceful fallback to demo data

### ✅ Auto-Refresh
- Refreshes data every 60 seconds
- Can be configured via `window.healthAPI.startAutoRefresh(intervalMs)`
- Stops on page unload

## Component Mapping

| React Component | Backend Data |
|----------------|--------------|
| `MetricCard` (Weight) | Calculated from health score |
| `MetricCard` (Food) | Random calories + trends |
| `StepsCircle` | Health score × 100 |
| `HeartRateCard` | `current_metrics.heart_rate` |
| `VitalSignCard` (Blood) | `current_metrics.blood_oxygen` |
| `VitalSignCard` (Temp) | `current_metrics.temperature` |
| `VitalSignCard` (Heart) | `current_metrics.heart_rate` |
| `OrganCard` (Heart) | Status based on heart rate range |
| `OrganCard` (Lungs) | Status based on respiration rate |
| `BodyDiagramCard` | Always displays body diagram |
| `SleepCard` | Static 7h 30m sleep data |

## Customization

### Change Refresh Interval
In `templates/dashboard.html`, modify:
```javascript
startAutoRefresh(60000); // 60 seconds
```

### Add New Metrics
1. Update Flask API to return new data
2. Modify `IndexBackendIntegrated.tsx` to use new data
3. Rebuild: `cd build-my-dashboard && npm run build`
4. Copy to static: `cp -r dist/* ../static/dashboard/`

### Update Styles
1. Edit Tailwind classes in `build-my-dashboard/src/`
2. Rebuild with `npm run build`
3. Copy updated CSS to static folder

## Development Workflow

### For React Changes:
```bash
cd build-my-dashboard

# Edit components in src/
# Then rebuild
npm run build

# Copy to Flask
cp -r dist/* ../static/dashboard/

# Update template if file hashes changed
# Check dist/index.html for new asset names
```

### For Backend Changes:
```bash
# Edit app.py or backend modules
# Restart Flask server
python app.py
```

## File Structure

```
Medical_app/
├── app.py                      # Flask app with /dashboard route
├── templates/
│   ├── index.html             # Original dashboard
│   └── dashboard.html         # React dashboard integration
├── static/
│   └── dashboard/             # Built React app
│       ├── index.html
│       └── assets/
│           ├── index-*.js     # React bundle
│           ├── index-*.css    # Styles
│           └── *.png          # Images
└── build-my-dashboard/        # React source code
    ├── src/
    │   ├── components/
    │   ├── pages/
    │   │   ├── Index.tsx                    # Original
    │   │   └── IndexBackendIntegrated.tsx   # With backend
    │   └── App.tsx            # Updated to use backend version
    ├── dist/                  # Build output
    └── package.json
```

## API Response Format

The backend returns data in this format:

```json
{
  "success": true,
  "dashboard": {
    "current_metrics": {
      "heart_rate": 98,
      "blood_oxygen": 102,
      "temperature": 37.1,
      "respiration_rate": 16,
      "health_score": 85
    },
    "status": {
      "anomaly": "Normal",
      "risk_level": "Low Risk"
    },
    "statistics": {
      "total_records": 100,
      "anomaly_count": 5,
      "avg_health_score": 83.5
    },
    "trends": {
      "heart_rate": [95, 98, 96, ...],
      "blood_oxygen": [99, 102, 100, ...],
      "temperature": [36.8, 37.1, 37.0, ...]
    }
  }
}
```

## Troubleshooting

### Dashboard not loading?
1. Check Flask server is running on port 5000
2. Verify `/dashboard` route returns 200
3. Check browser console for errors
4. Ensure static files are in `static/dashboard/`

### Data not updating?
1. Check browser console for API errors
2. Verify backend APIs are responding
3. Check `window.healthData` in browser console
4. Try manual refresh: `window.healthAPI.fetchData()`

### Build errors?
1. Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
2. Check Node.js version: `node --version` (should be v16+)
3. Clear build cache: `rm -rf dist`

## Next Steps

1. ✅ **Dashboard is live at http://localhost:5000/dashboard**
2. Customize components in `build-my-dashboard/src/`
3. Add more backend integrations
4. Implement user authentication
5. Add real-time WebSocket updates
6. Deploy to production

---

**Integration Complete!** 🎉

Your beautiful React dashboard is now powered by the AI backend!
