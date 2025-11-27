# 🏥 AI-Powered Health Monitoring System with Gemini Integration

An intelligent health monitoring system that uses **machine learning** and **Google's Gemini AI** to analyze wearable device data, detect health anomalies, and provide personalized health recommendations.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Gemini AI](https://img.shields.io/badge/Gemini-AI--Powered-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Key Features

### 🤖 **AI-Powered Insights** (NEW!)
- **Google Gemini Pro Integration** - Real AI-generated health recommendations
- **Context-Aware Analysis** - Considers historical trends and patterns
- **Personalized Advice** - Tailored to individual health metrics
- **Natural Language Insights** - Clear, empathetic communication

### 📊 **Advanced Analytics**
- **Anomaly Detection** - Isolation Forest algorithm identifies unusual patterns
- **Risk Assessment** - Random Forest classifier predicts health risk levels
- **Trend Analysis** - Track health metrics over time
- **Real-time Monitoring** - Instant analysis of incoming health data

### 💻 **Interactive Dashboard**
- **Beautiful UI** - Modern, responsive Bootstrap 5 design
- **Live Charts** - Chart.js visualizations for trends
- **Toast Notifications** - Real-time feedback for user actions
- **AI Status Indicators** - Know when you're getting AI vs rule-based insights

### 📱 **Comprehensive Health Metrics**
- Heart Rate monitoring
- Blood Oxygen (SpO2) levels
- Body Temperature tracking
- Respiration Rate analysis
- Activity Level assessment
- Overall Health Score calculation

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))
- Web browser

### Installation

1. **Clone/Navigate to the project:**
```bash
cd Medical_app
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure Gemini API:**

Create `.env` file from template:
```bash
cp .env.template .env
```

Edit `.env` and add your API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

4. **Verify Gemini integration:**
```bash
python verify_gemini.py
```

5. **Run the application:**
```bash
python app.py
```

6. **Open your browser:**
```
http://localhost:5000
```

### First Use

1. Enter a User ID (e.g., `user_001`)
2. Set number of records (default: 100)
3. Click **"Load Dashboard"**
4. View AI-powered health insights! 🎉

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [QUICK_START.md](QUICK_START.md) | 5-minute setup guide |
| [GEMINI_SETUP.md](GEMINI_SETUP.md) | Complete Gemini integration guide |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | REST API reference |

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Dashboard (UI)                      │
│              Bootstrap 5 + Chart.js + Vanilla JS            │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                   Flask REST API (Backend)                  │
│                     8 RESTful Endpoints                     │
└─────┬────────┬──────────────┬──────────────┬───────────────┘
      │        │              │              │
      ↓        ↓              ↓              ↓
┌──────────┐ ┌───────┐ ┌──────────┐ ┌──────────────────────┐
│ Gemini   │ │  ML   │ │  Data    │ │  Health              │
│ Advisor  │ │Models │ │Generator │ │  Recommendation      │
│          │ │       │ │          │ │  Engine              │
│ Google   │ │ ISO   │ │ Pandas   │ │  Rule-Based          │
│ Gemini   │ │Forest │ │ NumPy    │ │  Fallback            │
│ Pro API  │ │ RF    │ │          │ │                      │
└──────────┘ └───────┘ └──────────┘ └──────────────────────┘
```

### Tech Stack

**Backend:**
- Flask 3.0.0 - Web framework
- scikit-learn 1.3.2 - Machine learning
- Google Generative AI 0.3.2 - Gemini integration
- pandas 2.1.3 - Data manipulation
- python-dotenv 1.0.0 - Environment management

**Frontend:**
- Bootstrap 5 - UI framework
- Chart.js 4.4.0 - Data visualization
- Bootstrap Icons - Icon library
- Vanilla JavaScript - Client-side logic

**AI/ML Models:**
- **Isolation Forest** - Anomaly detection (unsupervised)
- **Random Forest Classifier** - Risk assessment (supervised)
- **Google Gemini Pro** - AI-powered insights generation

## 📁 Project Structure

```
Medical_app/
├── app.py                      # Main Flask application
├── gemini_advisor.py          # Gemini AI integration module ⭐ NEW
├── ml_models.py               # ML model implementations
├── health_data.py             # Data generation and preprocessing
├── requirements.txt           # Python dependencies
├── .env.template              # Environment variables template
├── .gitignore                 # Git ignore rules
├── verify_gemini.py           # Gemini verification script ⭐ NEW
│
├── templates/
│   └── index.html             # Enhanced dashboard UI ⭐ UPDATED
│
├── docs/
│   ├── README.md              # This file
│   ├── QUICK_START.md         # Quick setup guide ⭐ NEW
│   ├── GEMINI_SETUP.md        # Gemini integration guide ⭐ NEW
│   └── API_DOCUMENTATION.md   # API reference
│
└── tests/
    ├── quick_test.py          # Quick API tests
    ├── test_api.py            # Comprehensive API tests
    └── train_models.py        # Model training script
```

## 🔌 API Endpoints

### Health Monitoring

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health/dashboard/{user_id}` | GET | Complete dashboard with AI insights |
| `/api/health/realtime` | POST | Real-time health analysis |
| `/api/health/analyze` | POST | Comprehensive health analysis |
| `/api/health/simulate` | POST | Generate test health data |
| `/api/user/{user_id}/history` | GET | User's historical health data |

### Machine Learning

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/model/anomaly` | POST | Anomaly detection only |
| `/api/model/risk` | POST | Risk assessment only |
| `/api/model/info` | GET | Model information & Gemini status |

### Example Request

```bash
curl -X POST http://localhost:5000/api/health/realtime \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "heart_rate": 85,
    "blood_oxygen": 97,
    "temperature": 36.8,
    "respiration_rate": 16,
    "activity_level": "moderate"
  }'
```

### Example Response (with AI)

```json
{
  "success": true,
  "using_ai": true,
  "analysis": {
    "health_score": 85,
    "anomaly_status": "Normal",
    "risk_level": "Low Risk"
  },
  "ai_insights": {
    "summary": "Your vital signs are within healthy ranges...",
    "key_findings": [
      "Heart rate of 85 bpm is normal for moderate activity",
      "Excellent blood oxygen saturation at 97%",
      "Body temperature is optimal"
    ],
    "recommendations": [
      "Maintain current activity level",
      "Stay hydrated",
      "Continue monitoring regularly"
    ],
    "lifestyle_tips": [...],
    "monitoring_advice": "...",
    "when_to_seek_help": "...",
    "encouragement": "Great job maintaining your health!"
  }
}
```

## 🧪 Testing

### Verify Gemini Integration
```bash
python verify_gemini.py
```

### Test Individual Components
```bash
# Train ML models
python train_models.py

# Test all API endpoints
python test_api.py

# Quick API verification
python quick_test.py

# Test Gemini advisor directly
python gemini_advisor.py
```

## 🎨 UI Features

### Dashboard Components

1. **Header Section**
   - System title and last update timestamp
   - Responsive design for all devices

2. **User Input Panel**
   - User ID and record count configuration
   - Load Dashboard and Simulate Real-time buttons
   - Loading states and button feedback

3. **Current Metrics Cards**
   - Heart Rate (with ❤️ icon)
   - Blood Oxygen (with 💧 icon)
   - Temperature (with 🌡️ icon)
   - Respiration Rate (with 🌬️ icon)
   - Hover effects and animations

4. **Health Score Display**
   - Large circular score indicator
   - Color-coded by score level:
     - 🟢 Excellent (80-100)
     - 🟡 Good (60-79)
     - 🟠 Fair (40-59)
     - 🔴 Poor (0-39)
   - Anomaly and risk badges

5. **Statistics Panel**
   - Total records analyzed
   - Anomaly count
   - Average health score
   - Risk distribution chart

6. **Interactive Charts**
   - Heart Rate Trend (line chart)
   - Blood Oxygen Trend (line chart)
   - Health Score History (line chart)
   - Risk Distribution (doughnut chart)

7. **AI-Powered Recommendations** ⭐
   - 🤖 AI-Powered badge when using Gemini
   - 🔧 Rule-Based badge when using fallback
   - Comprehensive insight sections:
     - **Summary** - Overall health overview
     - **Key Findings** - Important observations
     - **Immediate Actions** - Urgent steps (if needed)
     - **Recommendations** - Actionable advice
     - **Lifestyle Tips** - Long-term wellness
     - **Monitoring Advice** - What to watch for
     - **When to Seek Help** - Medical consultation guidance
     - **Encouragement** - Positive message

8. **Toast Notifications**
   - Success notifications (green)
   - Error alerts (red)
   - Info messages (blue)
   - Auto-dismiss with close button

## 🔧 Configuration

### Environment Variables

Create a `.env` file with:

```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
FLASK_SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True
HOST=0.0.0.0
PORT=5000

# ML Model Configuration
ANOMALY_CONTAMINATION=0.05
RANDOM_STATE=42
```

### ML Model Tuning

Edit `ml_models.py` to adjust:

```python
# Anomaly detection sensitivity
self.anomaly_detector = IsolationForest(
    contamination=0.05,  # Expected % of anomalies
    random_state=42
)

# Risk classification thresholds
if health_score >= 80: return "Low Risk"
elif health_score >= 60: return "Medium Risk"
else: return "High Risk"
```

### Gemini Configuration

Edit `gemini_advisor.py` to customize:

```python
# Model selection
self.model = genai.GenerativeModel('gemini-pro')

# Generation parameters
generation_config = {
    "temperature": 0.7,  # Creativity level
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 2048
}

# Prompt customization
# See _create_health_analysis_prompt() method
```

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
pytest tests/

# Format code
black *.py

# Lint code
flake8 *.py
```

## ⚠️ Important Disclaimers

### Medical Disclaimer

> **⚠️ This system is for EDUCATIONAL and DEMONSTRATION purposes only.**
>
> - NOT intended for actual medical diagnosis or treatment
> - NOT a replacement for professional medical advice
> - NOT validated for clinical use
> - Always consult healthcare professionals for medical concerns

### Privacy & Data

- Health data is sent to Google's Gemini API for analysis
- Review [Google's Privacy Policy](https://policies.google.com/privacy)
- Do NOT use with real patient data without:
  - Proper informed consent
  - HIPAA compliance (if applicable)
  - Data anonymization
  - Legal review

### API Usage Limits

**Gemini Free Tier:**
- 60 requests per minute
- Monitor usage at: https://makersuite.google.com/

**Best Practices:**
- Implement rate limiting
- Use caching for repeated queries
- Monitor API quotas
- Consider paid tier for production

## 🐛 Troubleshooting

### Common Issues

**"GEMINI_API_KEY not found"**
```bash
# Solution: Check .env file exists and contains:
GEMINI_API_KEY=your_key_here
```

**"Connection test failed"**
```bash
# Solutions:
1. Check internet connection
2. Verify API key at https://makersuite.google.com/
3. Ensure API key has correct permissions
```

**"Module not found"**
```bash
# Solution: Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**"Port 5000 already in use"**
```bash
# Solution: Change port in app.py
app.run(host='0.0.0.0', port=5001, debug=True)
```

**"Using fallback recommendations"**
```bash
# This means Gemini isn't working. Check:
1. API key is set correctly in .env
2. Run: python verify_gemini.py
3. Check console logs for specific errors
4. Verify API quota hasn't been exceeded
```

### Debug Mode

Enable detailed logging:

```python
# In app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check browser console (F12) for client-side errors.

## 📊 Performance

### Benchmarks

- API Response Time: < 500ms (without Gemini)
- Gemini AI Generation: 2-5 seconds
- Anomaly Detection: < 100ms
- Risk Classification: < 50ms
- Dashboard Load: 1-3 seconds (100 records)

### Scalability

Current implementation:
- In-memory data storage
- Suitable for demos and prototypes
- 100-500 records per user

For production:
- Add database (PostgreSQL, MongoDB)
- Implement caching (Redis)
- Use message queues (RabbitMQ)
- Add load balancing

## 🗺️ Roadmap

### Coming Soon
- [ ] User authentication system
- [ ] Database integration (PostgreSQL)
- [ ] Mobile app (React Native)
- [ ] Email/SMS alerts for anomalies
- [ ] Export reports (PDF)
- [ ] Multi-language support

### Future Enhancements
- [ ] Wearable device integration (Fitbit, Apple Watch)
- [ ] Machine learning model improvements
- [ ] Predictive health analytics
- [ ] Social features (family sharing)
- [ ] Telemedicine integration

## 📚 Resources

### Documentation
- [Gemini API Docs](https://ai.google.dev/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [scikit-learn Guide](https://scikit-learn.org/stable/)
- [Chart.js Docs](https://www.chartjs.org/)

### Tutorials
- [Getting Started with Gemini](https://ai.google.dev/tutorials)
- [Flask REST API Tutorial](https://flask-restful.readthedocs.io/)
- [ML for Healthcare](https://www.coursera.org/learn/machine-learning-healthcare)

### Community
- [Gemini API Forum](https://discuss.ai.google.dev/)
- [Flask Community](https://discord.gg/flask)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/flask)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👏 Acknowledgments

- **Google Gemini AI** - For powerful AI insights
- **scikit-learn** - For machine learning tools
- **Flask** - For elegant web framework
- **Bootstrap** - For beautiful UI components
- **Chart.js** - For interactive visualizations

## 📧 Contact

For questions, issues, or suggestions:
- Open an issue on GitHub
- Check the documentation
- Review troubleshooting guide

---

**Made with ❤️ for better health monitoring**

*Last Updated: November 26, 2025*

---

## 🎯 Quick Links

- [Quick Start Guide](QUICK_START.md) - Get running in 5 minutes
- [Gemini Setup](GEMINI_SETUP.md) - Complete AI integration guide
- [API Documentation](API_DOCUMENTATION.md) - Full API reference
- [Verify Setup](verify_gemini.py) - Test your installation

**Ready to get started? Run:** `python verify_gemini.py`
