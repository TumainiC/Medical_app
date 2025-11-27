# API Documentation - Health Monitoring System

## Base URL
```
http://localhost:5000
```

## Endpoints

### 1. Simulate Health Data

Generate simulated health data for a user.

**Endpoint:** `POST /api/health/simulate`

**Request Body:**
```json
{
  "user_id": "user_001",
  "num_records": 100
}
```

**Response:**
```json
{
  "success": true,
  "message": "Generated 100 health records for user_001",
  "user_id": "user_001",
  "num_records": 100,
  "data": [...]
}
```

---

### 2. Analyze Health Data

Analyze stored health data for anomalies and risk assessment.

**Endpoint:** `POST /api/health/analyze`

**Request Body:**
```json
{
  "user_id": "user_001"
}
```

**Response:**
```json
{
  "success": true,
  "user_id": "user_001",
  "analysis": {
    "total_records": 100,
    "num_anomalies": 5,
    "anomaly_rate": 5.0,
    "avg_health_score": 87.5,
    "risk_distribution": {
      "Low Risk": 85,
      "Medium Risk": 10,
      "High Risk": 5
    }
  },
  "current_status": {
    "heart_rate": 75,
    "blood_oxygen": 98,
    "temperature": 36.6,
    "health_score": 90,
    "anomaly_status": "Normal",
    "risk_level": "Low Risk",
    "timestamp": "2025-11-26 10:30:00"
  },
  "recommendations": [
    "✅ Your vitals look good! Maintain healthy lifestyle habits.",
    "💧 Stay hydrated and get adequate rest."
  ],
  "detailed_results": [...]
}
```

---

### 3. Real-time Health Analysis

Analyze a single health record in real-time.

**Endpoint:** `POST /api/health/realtime`

**Request Body:**
```json
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

**Response:**
```json
{
  "success": true,
  "user_id": "user_001",
  "timestamp": "2025-11-26 10:30:00",
  "metrics": {
    "heart_rate": 75,
    "blood_oxygen": 98,
    "temperature": 36.6,
    "respiration_rate": 16,
    "activity_level": "moderate"
  },
  "analysis": {
    "health_score": 90,
    "anomaly_status": "Normal",
    "anomaly_score": 0.15,
    "risk_level": "Low Risk",
    "risk_probabilities": {
      "low": 0.85,
      "medium": 0.12,
      "high": 0.03
    }
  },
  "recommendations": [
    "✅ Your vitals look good! Maintain healthy lifestyle habits.",
    "💧 Stay hydrated and get adequate rest."
  ]
}
```

---

### 4. Get Dashboard Data

Get comprehensive dashboard data for a user.

**Endpoint:** `GET /api/health/dashboard/{user_id}`

**Parameters:**
- `user_id` (path): User identifier

**Response:**
```json
{
  "success": true,
  "dashboard": {
    "user_id": "user_001",
    "last_updated": "2025-11-26 10:30:00",
    "current_metrics": {
      "heart_rate": 75,
      "blood_oxygen": 98,
      "temperature": 36.6,
      "respiration_rate": 16,
      "health_score": 90
    },
    "status": {
      "anomaly": "Normal",
      "risk_level": "Low Risk"
    },
    "trends": {
      "heart_rate": [72, 75, 78, ...],
      "blood_oxygen": [97, 98, 98, ...],
      "temperature": [36.5, 36.6, 36.7, ...],
      "health_score": [88, 90, 92, ...],
      "timestamps": ["2025-11-26 10:00:00", ...]
    },
    "statistics": {
      "total_records": 100,
      "anomaly_count": 5,
      "avg_health_score": 87.5,
      "risk_distribution": {...}
    },
    "recommendations": [...]
  }
}
```

---

### 5. Get User History

Retrieve historical health data for a user.

**Endpoint:** `GET /api/health/history/{user_id}`

**Parameters:**
- `user_id` (path): User identifier
- `limit` (query): Number of records to return (default: 100)
- `start_date` (query, optional): Filter start date
- `end_date` (query, optional): Filter end date

**Example:**
```
GET /api/health/history/user_001?limit=50
```

**Response:**
```json
{
  "success": true,
  "user_id": "user_001",
  "num_records": 50,
  "data": [
    {
      "user_id": "user_001",
      "timestamp": "2025-11-26 10:00:00",
      "heart_rate": 75,
      "blood_oxygen": 98,
      "temperature": 36.6,
      "respiration_rate": 16,
      "activity_level": "moderate",
      "steps": 50,
      "sleep_quality": "good"
    },
    ...
  ]
}
```

---

### 6. Get User Statistics

Get statistical summary of user's health data.

**Endpoint:** `GET /api/health/statistics/{user_id}`

**Parameters:**
- `user_id` (path): User identifier

**Response:**
```json
{
  "success": true,
  "user_id": "user_001",
  "statistics": {
    "heart_rate": {
      "mean": 75.5,
      "min": 60,
      "max": 95,
      "std": 8.2
    },
    "blood_oxygen": {
      "mean": 97.8,
      "min": 95,
      "max": 100,
      "std": 1.5
    },
    "temperature": {
      "mean": 36.6,
      "min": 35.8,
      "max": 37.2,
      "std": 0.4
    },
    "activity_distribution": {
      "low": 30,
      "moderate": 50,
      "high": 20
    },
    "total_steps": 5000,
    "avg_steps_per_record": 50
  }
}
```

---

### 7. Export User Data

Export user's health data as CSV file.

**Endpoint:** `GET /api/health/export/{user_id}`

**Parameters:**
- `user_id` (path): User identifier

**Response:**
- Content-Type: `text/csv`
- File download with filename: `{user_id}_health_data_{date}.csv`

---

### 8. Get Model Information

Get information about the ML models.

**Endpoint:** `GET /api/model/info`

**Response:**
```json
{
  "success": true,
  "models": {
    "anomaly_detector": {
      "type": "Isolation Forest",
      "contamination": 0.05,
      "feature_importance": {
        "heart_rate": 0.25,
        "blood_oxygen": 0.22,
        "temperature": 0.18,
        "respiration_rate": 0.15,
        "activity_level_encoded": 0.12,
        "steps": 0.08
      }
    },
    "risk_classifier": {
      "type": "Random Forest Classifier",
      "risk_levels": ["Low Risk", "Medium Risk", "High Risk"],
      "feature_importance": {...}
    }
  }
}
```

---

## Error Responses

All endpoints return error responses in the following format:

```json
{
  "success": false,
  "error": "Error message description"
}
```

**HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (invalid input)
- `404` - Not Found (user/data not found)
- `500` - Internal Server Error

---

## Health Metric Ranges

### Normal Ranges:

- **Heart Rate**: 60-100 bpm
- **Blood Oxygen**: 95-100%
- **Temperature**: 36.1-37.2°C
- **Respiration Rate**: 12-20 breaths/min

### Risk Assessment Criteria:

**High Risk:**
- Heart Rate: <50 or >120 bpm
- Blood Oxygen: <90%
- Temperature: <35.5 or >38.0°C

**Medium Risk:**
- Heart Rate: 50-60 or 100-120 bpm
- Blood Oxygen: 90-95%
- Temperature: 35.5-36.1 or 37.2-38.0°C

**Low Risk:**
- All metrics within normal ranges

---

## Examples

### Python Example

```python
import requests
import json

BASE_URL = "http://localhost:5000"

# Simulate data
response = requests.post(
    f"{BASE_URL}/api/health/simulate",
    json={"user_id": "user_001", "num_records": 100}
)
print(response.json())

# Get dashboard
response = requests.get(f"{BASE_URL}/api/health/dashboard/user_001")
dashboard = response.json()
print(f"Health Score: {dashboard['dashboard']['current_metrics']['health_score']}")
```

### JavaScript Example

```javascript
// Real-time analysis
async function analyzeHealth(data) {
  const response = await fetch('http://localhost:5000/api/health/realtime', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  
  const result = await response.json();
  console.log('Health Score:', result.analysis.health_score);
  console.log('Risk Level:', result.analysis.risk_level);
}

// Usage
analyzeHealth({
  user_id: 'user_001',
  heart_rate: 75,
  blood_oxygen: 98,
  temperature: 36.6,
  respiration_rate: 16,
  activity_level: 'moderate',
  steps: 50,
  sleep_quality: 'good'
});
```

### cURL Examples

```bash
# Simulate data
curl -X POST http://localhost:5000/api/health/simulate \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_001", "num_records": 100}'

# Get dashboard
curl http://localhost:5000/api/health/dashboard/user_001

# Real-time analysis
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

# Export data
curl http://localhost:5000/api/health/export/user_001 -o health_data.csv
```

---

## Rate Limiting

Currently, there are no rate limits implemented. For production deployment, consider implementing rate limiting using Flask-Limiter:

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@limiter.limit("100 per hour")
@app.route('/api/health/analyze', methods=['POST'])
def analyze_health_data():
    # ...
```

---

## Authentication

The current implementation does not include authentication. For production:

1. Implement JWT token authentication
2. Add API key validation
3. Use OAuth2 for third-party integrations
4. Implement user roles and permissions

---

## CORS Configuration

CORS is enabled for all origins in development. For production, restrict origins:

```python
CORS(app, resources={r"/api/*": {"origins": ["https://your-domain.com"]}})
```
