# Quick Start Guide - AI Health Monitoring System

## 🚀 Getting Started in 5 Minutes

### Prerequisites Check
```bash
python --version  # Should be 3.8+
pip --version
```

### Installation

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Run the application**
```bash
python app.py
```

3. **Open your browser**
```
http://localhost:5000
```

That's it! You're ready to go! 🎉

---

## 📋 Quick Commands Reference

### Run Flask Web App
```bash
python app.py
```

### Run Streamlit Version
```bash
streamlit run index.py
```

### Train Models
```bash
python train_models.py
```

### Test API
```bash
python test_api.py
```

### Test Individual Modules
```bash
python health_data.py
python ml_models.py
```

---

## 🎮 Quick Usage Tutorial

### Web Dashboard

1. **Enter User ID**: Type a user ID (e.g., `user_001`)
2. **Set Records**: Choose how many data points to generate (default: 100)
3. **Click "Load Dashboard"**: System will:
   - Generate simulated health data
   - Train ML models (first time only)
   - Analyze data for anomalies
   - Display results and recommendations
4. **Try Real-time**: Click "Simulate Real-time Data" for instant analysis

### Using the API

**Simulate Data:**
```bash
curl -X POST http://localhost:5000/api/health/simulate \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_001", "num_records": 100}'
```

**Get Dashboard:**
```bash
curl http://localhost:5000/api/health/dashboard/user_001
```

**Real-time Analysis:**
```bash
curl -X POST http://localhost:5000/api/health/realtime \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "heart_rate": 75,
    "blood_oxygen": 98,
    "temperature": 36.6,
    "respiration_rate": 16,
    "activity_level": "moderate",
    "steps": 50,
    "sleep_quality": "good"
  }'
```

---

## 📊 What You'll See

### Dashboard Features:

1. **Current Metrics Cards**
   - Heart Rate (bpm)
   - Blood Oxygen (%)
   - Temperature (°C)
   - Respiration Rate

2. **Health Score Circle**
   - Overall health score (0-100)
   - Color-coded: Green (excellent) → Red (poor)

3. **Status Indicators**
   - Anomaly Status: Normal or Anomaly
   - Risk Level: Low, Medium, or High Risk

4. **Interactive Charts**
   - Heart rate trends over time
   - Blood oxygen trends
   - Health score history

5. **Personalized Recommendations**
   - AI-generated health advice
   - Alerts for abnormal readings
   - Action items

---

## 🔧 Common Issues & Solutions

### Issue: Port 5000 already in use
**Solution:**
```python
# Edit app.py, change the last line to:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: Import errors
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Issue: No module named 'flask'
**Solution:**
```bash
pip install flask flask-cors
```

### Issue: Models not training
**Solution:**
```bash
mkdir models
python train_models.py
```

---

## 🎯 Next Steps

1. **Explore the API**: Try different endpoints with Postman
2. **Customize Models**: Edit parameters in `ml_models.py`
3. **Add Features**: Extend the system with your own ideas
4. **Deploy**: Follow deployment guides in README.md
5. **Integrate Wearables**: Connect real device data

---

## 📚 File Structure

```
Medical_app/
├── app.py                 ← Main Flask application
├── health_data.py        ← Data simulation & preprocessing
├── ml_models.py          ← Machine learning models
├── train_models.py       ← Training script
├── test_api.py           ← API testing script
├── index.py              ← Streamlit version
├── requirements.txt      ← Dependencies
├── templates/
│   └── index.html       ← Web dashboard
└── models/              ← Saved ML models (auto-generated)
```

---

## 💡 Tips & Tricks

### Tip 1: Fast Iteration
During development, keep Flask in debug mode:
```python
app.run(debug=True)  # Auto-reloads on code changes
```

### Tip 2: Better Logging
Add logging to track system behavior:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Tip 3: Database Integration
For production, replace in-memory storage with a database:
```python
# Instead of: user_data_store = {}
# Use: SQLAlchemy or MongoDB
```

### Tip 4: Environment Variables
Use `.env` file for configuration:
```bash
FLASK_SECRET_KEY=your-secret-key
FLASK_ENV=development
```

---

## 🆘 Getting Help

1. **Check README.md** for detailed documentation
2. **Review code comments** in Python files
3. **Run with debug mode** to see detailed errors
4. **Test API endpoints** with `test_api.py`

---

## 🎓 Learning Path

1. ✅ **Install & Run** (You are here!)
2. 📊 **Understand the Data** - Check `health_data.py`
3. 🤖 **Explore ML Models** - Review `ml_models.py`
4. 🌐 **Study the API** - Read `app.py`
5. 💻 **Customize UI** - Modify `templates/index.html`
6. 🚀 **Deploy** - Follow deployment guides

---

**Happy Coding! 🎉**

For detailed documentation, see **README.md**
