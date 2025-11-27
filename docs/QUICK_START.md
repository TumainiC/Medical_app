# Quick Setup Guide - AI Health Monitoring System

## 📋 Prerequisites

- Python 3.8 or higher
- Google Gemini API Key (get from https://makersuite.google.com/app/apikey)
- Web browser (Chrome, Firefox, Edge, or Safari)

## 🚀 Quick Start (5 Minutes)

### Step 1: Set Up Environment

```bash
# Navigate to project directory
cd Medical_app

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Gemini API

**Option A: Using .env file (Recommended)**

1. Create `.env` file from template:
```bash
cp .env.template .env
```

2. Edit `.env` and add your API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

**Option B: Set environment variable directly**

Windows (Command Prompt):
```cmd
set GEMINI_API_KEY=your_api_key_here
```

Windows (PowerShell):
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

Linux/Mac:
```bash
export GEMINI_API_KEY=your_api_key_here
```

### Step 3: Test Gemini Connection

```bash
python gemini_advisor.py
```

You should see:
```
✓ Connected to Gemini AI successfully!
📊 AI-GENERATED HEALTH INSIGHTS
...
```

### Step 4: Run the Application

```bash
python app.py
```

The server will start at: **http://localhost:5000**

### Step 5: Open the Dashboard

1. Open your web browser
2. Navigate to: **http://localhost:5000**
3. Click "Load Dashboard" button
4. View AI-powered health insights! 🎉

## 🧪 Testing

### Test Individual Components

```bash
# Test ML models
python train_models.py

# Test API endpoints
python test_api.py

# Quick API test
python quick_test.py
```

### Test Gemini Integration

```bash
# Direct Gemini test
python gemini_advisor.py

# Check if API key is loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key loaded:', 'Yes' if os.getenv('GEMINI_API_KEY') else 'No')"
```

## 🔍 Troubleshooting

### Issue: "GEMINI_API_KEY not found"

**Solution:**
1. Check if `.env` file exists in project root
2. Verify the file contains: `GEMINI_API_KEY=your_key_here`
3. No spaces around the `=` sign
4. No quotes around the key value

### Issue: "Connection test failed"

**Solutions:**
1. Check internet connection
2. Verify API key is valid at https://makersuite.google.com/
3. Make sure you copied the entire key (starts with `AIza...`)
4. Check if API is enabled for your Google account

### Issue: "Module not found"

**Solution:**
```bash
pip install --upgrade -r requirements.txt
```

### Issue: Port 5000 already in use

**Solution:**
Change the port in `app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)  # Use port 5001
```

## 📊 Understanding the Dashboard

### Metrics Displayed

- **Heart Rate**: Normal range 60-100 bpm
- **Blood Oxygen**: Normal range 95-100%
- **Temperature**: Normal range 36.1-37.2°C
- **Respiration**: Normal range 12-20 breaths/min
- **Health Score**: 0-100 (higher is better)

### Status Indicators

- **🟢 Normal**: All metrics within healthy range
- **🔴 Anomaly**: One or more metrics outside normal range
- **Low Risk**: Minimal health concerns
- **Medium Risk**: Some attention needed
- **High Risk**: Medical consultation recommended

### AI Features

When Gemini is active, you'll see:
- 🤖 **AI-Powered Insights** badge
- Detailed summary of your health status
- Key findings from data analysis
- Personalized recommendations
- Lifestyle tips for long-term wellness
- Monitoring advice
- When to seek medical help

## 🎯 Common Tasks

### Generate Health Data

1. Enter User ID (e.g., `user_001`)
2. Set number of records (default: 100)
3. Click "Load Dashboard"

### Simulate Real-time Monitoring

1. Enter User ID
2. Click "Simulate Real-time Data"
3. View instant AI analysis in popup

### Switch Between Users

1. Change User ID in input field
2. Click "Load Dashboard" again
3. View different user's health data

## 📝 API Endpoints

All endpoints return JSON responses.

### Dashboard Data
```
GET /api/health/dashboard/{user_id}
```

### Real-time Analysis
```
POST /api/health/realtime
Body: { user_id, heart_rate, blood_oxygen, temperature, respiration_rate }
```

### Generate Data
```
POST /api/health/simulate
Body: { user_id, num_records }
```

### Health Analysis
```
POST /api/health/analyze
Body: { user_id, heart_rate, blood_oxygen, temperature, respiration_rate }
```

### Model Info
```
GET /api/model/info
```

### Anomaly Detection
```
POST /api/model/anomaly
Body: { user_id, heart_rate, blood_oxygen, temperature, respiration_rate }
```

### Risk Assessment
```
POST /api/model/risk
Body: { user_id, heart_rate, blood_oxygen, temperature, respiration_rate }
```

### User History
```
GET /api/user/{user_id}/history
```

## 🔧 Configuration

### Environment Variables (.env)

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key

# Optional
FLASK_SECRET_KEY=your-secret-key
FLASK_ENV=development
FLASK_DEBUG=True
HOST=0.0.0.0
PORT=5000
```

### ML Model Settings

Edit `ml_models.py` to adjust:
- Anomaly detection sensitivity
- Risk classification thresholds
- Feature importance weights

## 📚 Additional Documentation

- **Full Setup Guide**: See `GEMINI_SETUP.md`
- **API Documentation**: See `API_DOCUMENTATION.md`
- **Project README**: See `README.md`

## 🆘 Need Help?

1. Check console logs in terminal
2. Open browser developer tools (F12)
3. Review error messages
4. Verify all dependencies are installed
5. Test Gemini connection with `python gemini_advisor.py`

## 🎓 Learning Resources

- **Gemini API Docs**: https://ai.google.dev/docs
- **Flask Documentation**: https://flask.palletsprojects.com/
- **Chart.js**: https://www.chartjs.org/
- **Bootstrap 5**: https://getbootstrap.com/

## ⚠️ Important Notes

### Medical Disclaimer
- This is a **demonstration system** for educational purposes
- **NOT** intended for actual medical diagnosis or treatment
- Always consult healthcare professionals for medical advice
- Do not use with real patient data without proper consent and HIPAA compliance

### API Limits
- Gemini free tier: 60 requests/minute
- Monitor usage at: https://makersuite.google.com/

### Data Privacy
- Health data is sent to Gemini API for analysis
- Review Google's privacy policy
- Consider data anonymization for production use

---

**✅ Setup Complete! Enjoy your AI-powered health monitoring system!**

*Last Updated: November 26, 2025*
