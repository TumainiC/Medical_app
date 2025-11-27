# AI-Powered Health Monitoring System

## Project Overview

This is a comprehensive AI-powered health monitoring system that analyzes real-time health data from wearable devices to detect anomalies and provide personalized health recommendations. The system uses machine learning algorithms to identify abnormal health conditions and assess risk levels.

## Key Features

- **Real-Time Health Monitoring**: Collect and analyze health metrics continuously
- **Anomaly Detection**: AI-powered detection of abnormal health patterns using Isolation Forest
- **Risk Assessment**: Multi-level risk classification (Low, Medium, High) using Random Forest
- **Personalized Recommendations**: Context-aware health advice based on current metrics
- **Interactive Dashboard**: User-friendly web interface with real-time visualizations
- **REST API**: Comprehensive API for integration with mobile apps and wearable devices
- **Data Export**: Export health data and reports in CSV format

## Monitored Health Metrics

1. **Heart Rate** (bpm) - Normal range: 60-100
2. **Blood Oxygen Saturation** (%) - Normal range: 95-100
3. **Body Temperature** (°C) - Normal range: 36.1-37.2
4. **Respiration Rate** (breaths/min) - Normal range: 12-20
5. **Activity Level** - Low, Moderate, High
6. **Steps Count**
7. **Sleep Quality** - Poor, Fair, Good, Excellent

## System Architecture

```
Medical_app/
├── app.py                      # Flask web application (entry point)
├── requirements.txt            # Python dependencies
├── .env                        # Environment configuration
│
├── src/                        # Source code (organized packages)
│   ├── core/                   # Core business logic
│   │   ├── health_data.py      # Data simulation & preprocessing
│   │   └── ml_models.py        # ML models (Anomaly Detection, Risk Classification)
│   ├── ai/                     # AI integration
│   │   └── gemini_advisor.py   # Google Gemini AI for health insights
│   └── utils/                  # Utility functions
│
├── tests/                      # Test files
│   ├── test_api.py            # API endpoint tests
│   ├── test_streaming.py      # Streaming functionality tests
│   ├── quick_test.py          # Quick smoke tests
│   └── verify_gemini.py       # Gemini integration verification
│
├── scripts/                    # Utility scripts
│   ├── train_models.py        # Model training
│   └── cleanup_models.py      # Model cleanup
│
├── templates/                  # HTML templates
│   └── index.html             # Web dashboard interface
│
├── static/                     # Static assets
│
├── models/                     # Trained ML models (auto-generated)
│   ├── anomaly_detector.pkl
│   ├── risk_classifier.pkl
│   └── scaler.pkl
│
└── docs/                       # Documentation
    ├── README.md              # This file
    ├── PROJECT_STRUCTURE.md   # Detailed project structure guide
    ├── QUICK_START.md         # 5-minute setup guide
    ├── GEMINI_SETUP.md        # AI integration guide
    └── API_DOCUMENTATION.md   # API reference
```

> 📖 **For detailed project structure information**, see [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

## Installation and Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone or Download the Project

```bash
cd Medical_app
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

#### Option 1: Flask Web Application (Recommended)

```bash
python app.py
```

Access the application at: **http://localhost:5000**

#### Option 2: Streamlit Application

```bash
streamlit run index.py
```

Access the application at: **http://localhost:8501**

## Usage Guide

### Web Dashboard

1. **Open your browser** and navigate to `http://localhost:5000`
2. **Enter User ID** (e.g., user_001) and number of records to generate
3. **Click "Load Dashboard"** to simulate and analyze health data
4. **View Results**:
   - Current health metrics
   - Overall health score
   - Anomaly status and risk level
   - Historical trends (charts)
   - Personalized recommendations
5. **Try Real-time Analysis** with "Simulate Real-time Data" button

### REST API Endpoints

#### 1. Simulate Health Data
```http
POST /api/health/simulate
Content-Type: application/json

{
  "user_id": "user_001",
  "num_records": 100
}
```

#### 2. Analyze Health Data
```http
POST /api/health/analyze
Content-Type: application/json

{
  "user_id": "user_001"
}
```

#### 3. Real-time Analysis
```http
POST /api/health/realtime
Content-Type: application/json

{
  "user_id": "user_001",
  "heart_rate": 75,
  "blood_oxygen": 98,
  "temperature": 36.6,
  "respiration_rate": 16,
  "activity_level": "moderate",
  "steps": 50,
  "sleep_quality": "good"
}
```

#### 4. Get Dashboard Data
```http
GET /api/health/dashboard/{user_id}
```

#### 5. Get User History
```http
GET /api/health/history/{user_id}?limit=100
```

#### 6. Get Statistics
```http
GET /api/health/statistics/{user_id}
```

#### 7. Export Data
```http
GET /api/health/export/{user_id}
```

#### 8. Get Model Information
```http
GET /api/model/info
```

## Machine Learning Models

### 1. Anomaly Detection Model

**Algorithm**: Isolation Forest  
**Purpose**: Detect abnormal patterns in health metrics  
**Features Used**:
- Heart rate
- Blood oxygen saturation
- Body temperature
- Respiration rate
- Activity level
- Step count

**Output**: Normal or Anomaly classification

### 2. Risk Classification Model

**Algorithm**: Random Forest Classifier  
**Purpose**: Classify health risk levels  
**Risk Levels**:
- Low Risk: All metrics within normal ranges
- Medium Risk: Some metrics slightly outside normal ranges
- High Risk: Multiple metrics significantly abnormal

**Output**: Risk level (Low/Medium/High) with probability scores

### 3. Recommendation Engine

**Purpose**: Generate personalized health recommendations  
**Input**: Current health metrics, anomaly status, risk level  
**Output**: Actionable health advice and alerts

## Model Performance

### Anomaly Detection
- **Contamination Rate**: 5% (configurable)
- **Detection Method**: Unsupervised learning
- **Training Data**: 2000+ simulated health records

### Risk Classification
- **Accuracy**: ~85-90% on test data
- **Classes**: 3 (Low, Medium, High Risk)
- **Features**: 6 health metrics
- **Training Method**: Supervised learning with balanced classes

## Configuration

### Model Parameters

Edit in `ml_models.py`:

```python
# Anomaly Detector
anomaly_detector = HealthAnomalyDetector(contamination=0.05)

# Risk Classifier
risk_classifier = HealthRiskClassifier()
```

### Health Score Calculation

Edit `calculate_health_score()` function in `health_data.py` to adjust scoring logic.

## Mobile App Integration

The REST API is designed for easy integration with mobile applications:

1. **Enable CORS**: Already configured in `app.py`
2. **API Endpoints**: Use the documented REST endpoints
3. **Authentication**: Add JWT or OAuth in production
4. **Real-time Updates**: Implement WebSocket for live monitoring

### Example Mobile Integration

```javascript
// Send health data from wearable
async function sendHealthData(data) {
  const response = await fetch('http://your-server:5000/api/health/realtime', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return await response.json();
}
```

## Cloud Deployment

### Deploy on Azure

1. **Create Azure App Service**
2. **Configure Python runtime**
3. **Deploy using Git or Azure CLI**:

```bash
az webapp up --name health-monitor-app --resource-group myResourceGroup
```

### Deploy on AWS (EC2)

1. **Launch EC2 instance** (Ubuntu)
2. **Install dependencies**:
```bash
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt
```
3. **Run with Gunicorn**:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Deploy on Heroku

1. **Create `Procfile`**:
```
web: gunicorn app:app
```
2. **Deploy**:
```bash
heroku create health-monitor
git push heroku main
```

## Security and Privacy

### Data Privacy Considerations

- **GDPR Compliance**: Implement user consent and data deletion
- **HIPAA Compliance**: Encrypt data in transit and at rest
- **Data Anonymization**: Remove PII before analysis
- **Secure Storage**: Use encrypted databases

### Security Best Practices

1. **Use HTTPS** in production
2. **Implement authentication** (JWT, OAuth2)
3. **Validate input data** to prevent injection attacks
4. **Rate limiting** on API endpoints
5. **Secure model files** with encryption
6. **Regular security audits**

## Testing

### Run Unit Tests

```bash
# Test data generation
python health_data.py

# Test ML models
python ml_models.py

# Test API endpoints (requires app running)
pytest tests/
```

### Manual Testing

1. **Test Normal Data**: Generate data with normal metrics
2. **Test Anomalies**: Manually create records with extreme values
3. **Test API**: Use Postman or curl to test endpoints
4. **Load Testing**: Use tools like Apache JMeter

## Troubleshooting

### Issue: Models not training

**Solution**: Check if `models/` directory exists and has write permissions

```bash
mkdir models
```

### Issue: Import errors

**Solution**: Ensure all dependencies are installed

```bash
pip install -r requirements.txt --upgrade
```

### Issue: Port already in use

**Solution**: Change port in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: Charts not displaying

**Solution**: Ensure JavaScript is enabled and check browser console for errors

## Project Documentation

### Code Structure

- **health_data.py**: Data simulation and preprocessing logic
- **ml_models.py**: Machine learning model implementations
- **app.py**: Flask application with REST API endpoints
- **index.html**: Frontend dashboard with charts

### Key Classes

1. `HealthDataSimulator`: Generates realistic health data
2. `HealthDataPreprocessor`: Prepares data for ML models
3. `HealthAnomalyDetector`: Detects anomalies using Isolation Forest
4. `HealthRiskClassifier`: Classifies risk levels
5. `HealthRecommendationEngine`: Generates personalized advice

## Learning Outcomes

This project demonstrates:

- Machine learning for healthcare applications
- Anomaly detection using unsupervised learning
- Risk classification using supervised learning
- RESTful API design
- Full-stack web development with Flask
- Data visualization with Chart.js
- Real-time data processing

## Future Enhancements

1. **Deep Learning**: Implement LSTM for time-series prediction
2. **Wearable Integration**: Connect to real devices (Fitbit, Apple Watch)
3. **Database**: Add PostgreSQL or MongoDB for data persistence
4. **User Authentication**: Implement secure login system
5. **Mobile App**: Develop native iOS/Android apps
6. **Telemedicine**: Integrate video consultation features
7. **Alert System**: Send SMS/email notifications for critical alerts
8. **Multi-language Support**: Internationalization
9. **Advanced Analytics**: Trends, predictions, correlations
10. **Doctor Dashboard**: Separate interface for healthcare providers

## Contributors

- **Cindy Tumaini** - Initial development

## License

This project is for educational purposes. Consult with medical professionals before using in production healthcare environments.

## Support

For issues, questions, or contributions:
1. Open an issue on GitHub
2. Submit a pull request
3. Contact the maintainer

## Contact

- **Email**: your.email@example.com
- **GitHub**: github.com/yourusername
- **LinkedIn**: linkedin.com/in/yourprofile

---

**Medical Disclaimer**: This system is for educational and demonstration purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of qualified health providers with any questions regarding medical conditions.

---

**Built with using Python, Flask, scikit-learn, and Chart.js**
