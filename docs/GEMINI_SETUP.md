# Gemini AI Integration Guide

## 🤖 Overview

The Health Monitoring System now integrates with **Google's Gemini AI** to provide intelligent, context-aware health recommendations and insights. Instead of simple rule-based recommendations, you now get personalized AI-powered analysis!

## ✨ What's New

### Before (Rule-Based)
- ❌ Generic recommendations
- ❌ Simple if-then rules
- ❌ No context awareness
- ❌ Limited personalization

### After (AI-Powered)
- ✅ **Intelligent Analysis** - Gemini understands complex health patterns
- ✅ **Personalized Insights** - Recommendations tailored to your specific metrics
- ✅ **Trend Analysis** - AI considers historical data trends
- ✅ **Comprehensive Reports** - Detailed findings, lifestyle tips, and encouragement
- ✅ **Natural Language** - Clear, empathetic communication

## 🚀 Setup Instructions

### Step 1: Get Gemini API Key

1. **Visit Google AI Studio**
   - Go to: https://makersuite.google.com/app/apikey
   
2. **Sign in** with your Google account

3. **Create API Key**
   - Click "Get an API key" or "Create API key"
   - Select "Create API key in new project" (or use existing)
   - Copy the generated key (starts with `AIza...`)

### Step 2: Configure Environment

**Option A: Using .env file (Recommended)**

1. Create a `.env` file in the project root:
   ```bash
   cp .env.template .env
   ```

2. Edit `.env` and add your API key:
   ```bash
   GEMINI_API_KEY=AIzaSyB1a2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
   ```

**Option B: Environment Variable**

```bash
# Windows (Command Prompt)
set GEMINI_API_KEY=your_api_key_here

# Windows (PowerShell)
$env:GEMINI_API_KEY="your_api_key_here"

# Linux/Mac
export GEMINI_API_KEY=your_api_key_here
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `google-generativeai` - Gemini API client
- `python-dotenv` - Environment variable management

### Step 4: Test Gemini Connection

```bash
python gemini_advisor.py
```

You should see:
```
✓ Connected to Gemini AI successfully!
📊 AI-GENERATED HEALTH INSIGHTS
...
```

### Step 5: Run the Application

```bash
python app.py
```

The application will automatically detect and use Gemini AI!

## 📊 AI-Powered Features

### 1. Comprehensive Insights Structure

When Gemini analyzes your health data, you get:

```json
{
  "summary": "Brief overview of your health status",
  "key_findings": [
    "Finding about your vitals",
    "Patterns or concerns",
    "Positive aspects"
  ],
  "recommendations": [
    "Specific actionable steps",
    "Lifestyle modifications",
    "Health improvements"
  ],
  "immediate_actions": [
    "Urgent actions (if needed)"
  ],
  "lifestyle_tips": [
    "Long-term wellness advice",
    "Prevention strategies"
  ],
  "monitoring_advice": "What to watch for",
  "when_to_seek_help": "When to contact healthcare provider",
  "encouragement": "Positive message"
}
```

### 2. Trend Analysis

Gemini considers your last 20 health readings to understand:
- Whether metrics are improving or declining
- Unusual patterns or fluctuations
- Overall health trajectory

### 3. Context-Aware Recommendations

The AI considers:
- Current vital signs
- Anomaly detection results
- Risk assessment level
- Historical trends
- Activity levels
- Overall health score

## 🎯 How It Works

### API Endpoints with AI

All analysis endpoints now include `using_ai` and `ai_insights` fields:

**1. Real-time Analysis**
```bash
POST /api/health/realtime
```
Response includes:
- `using_ai`: boolean (true if Gemini was used)
- `ai_insights`: complete Gemini analysis
- `recommendations`: AI-generated recommendations

**2. Dashboard**
```bash
GET /api/health/dashboard/{user_id}
```
Dashboard data includes AI-powered insights!

**3. Health Analysis**
```bash
POST /api/health/analyze
```
Full analysis with AI recommendations

### Fallback Mechanism

**Smart Fallback:**
- If Gemini is unavailable → Falls back to rule-based
- If API limit reached → Uses rule-based temporarily
- If network error → Continues with local recommendations

You'll see warnings in the console:
```
⚠️  Gemini failed, using fallback: [reason]
```

## 💻 Web UI Integration

### AI Status Indicator

The dashboard shows:
- 🤖 **"AI-Powered Insights"** badge when using Gemini
- 🔧 **"Rule-Based"** badge when using fallback

### Enhanced Recommendations Display

When AI is active, you'll see:
- **Summary** section with overview
- **Key Findings** with bullet points
- **Actionable Recommendations**
- **Lifestyle Tips** for long-term health
- **Monitoring Advice**
- **When to Seek Help** guidance
- **Encouragement** message

## 🔍 Testing

### Test Gemini Integration

```bash
# Test the Gemini advisor directly
python gemini_advisor.py

# Test with quick verification script
python quick_test.py
```

### Test API with Gemini

```bash
# Test all endpoints
python test_api.py
```

### Check Logs

When running the app, watch for:
```
✓ Gemini AI module imported successfully
✓ Gemini Health Advisor initialized
🤖 Generating AI-powered insights with Gemini...
✓ Gemini AI insights generated successfully
```

## 📱 Example Usage

### Python Example

```python
from gemini_advisor import GeminiHealthAdvisor

advisor = GeminiHealthAdvisor()

health_data = {
    'heart_rate': 145,
    'blood_oxygen': 94,
    'temperature': 37.8,
    'respiration_rate': 22,
    'activity_level': 'high',
    'health_score': 72
}

insights = advisor.generate_comprehensive_insights(
    health_data=health_data,
    anomaly_status='Anomaly',
    risk_level='Medium Risk'
)

print(insights['summary'])
for rec in insights['recommendations']:
    print(f"• {rec}")
```

### API Example

```bash
curl -X POST http://localhost:5000/api/health/realtime \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_001",
    "heart_rate": 145,
    "blood_oxygen": 94,
    "temperature": 37.8,
    "respiration_rate": 22,
    "activity_level": "high"
  }'
```

Response will include AI insights!

## ⚠️ Important Notes

### API Limits

**Free Tier:**
- 60 requests per minute
- Should be sufficient for normal use

**Best Practices:**
- Don't make excessive requests
- Use caching for repeated queries
- Monitor your usage at: https://makersuite.google.com/

### Privacy & Safety

**Medical Disclaimer:**
- Gemini provides insights, NOT medical diagnoses
- Always consult healthcare professionals for medical advice
- The AI is a wellness advisor, not a replacement for doctors

**Data Privacy:**
- Health data sent to Gemini API for analysis
- Review Google's privacy policy
- Do not use with real patient data in production without proper consent
- Consider HIPAA compliance requirements

### Error Handling

The system handles errors gracefully:
- Invalid API key → Falls back to rule-based
- Network timeout → Uses fallback recommendations
- Rate limit exceeded → Temporary rule-based mode
- All errors logged for debugging

## 🔧 Troubleshooting

### Issue: "GEMINI_API_KEY not found"

**Solution:**
```bash
# Check if .env exists
ls -la .env

# Verify content
cat .env

# Make sure it contains:
GEMINI_API_KEY=your_actual_key_here
```

### Issue: "Connection test failed"

**Solutions:**
1. Check internet connection
2. Verify API key is valid
3. Check if API key has required permissions
4. Visit https://makersuite.google.com/ to verify status

### Issue: "Using fallback recommendations"

**This means:**
- API key not configured (check .env)
- Network issues (check connection)
- API limits reached (wait a minute)
- Invalid API key (get new one)

**To fix:**
1. Check console logs for specific error
2. Verify API key in .env
3. Test with `python gemini_advisor.py`
4. Check Google AI Studio for API status

### Issue: Import errors

**Solution:**
```bash
pip install --upgrade google-generativeai python-dotenv
```

## 📚 Advanced Configuration

### Custom Prompts

Edit `gemini_advisor.py` to customize:
- System context
- Prompt structure
- Response format
- Analysis depth

### Model Selection

Currently using `gemini-pro`. To use other models:

```python
self.model = genai.GenerativeModel('gemini-pro')  # Current
# self.model = genai.GenerativeModel('gemini-ultra')  # When available
```

### Caching Responses

To reduce API calls, implement caching:

```python
from functools import lru_cache
import hashlib
import json

@lru_cache(maxsize=100)
def cached_insights(health_data_json, anomaly_status, risk_level):
    health_data = json.loads(health_data_json)
    return advisor.generate_comprehensive_insights(...)
```

## 🎓 Learning Resources

- **Gemini API Docs**: https://ai.google.dev/docs
- **API Reference**: https://ai.google.dev/api/python
- **Examples**: https://github.com/google/generative-ai-python
- **Best Practices**: https://ai.google.dev/docs/concepts

## 📞 Support

**If you encounter issues:**
1. Check the console logs
2. Run `python gemini_advisor.py` for diagnostics
3. Verify API key setup
4. Review error messages in logs

**Gemini API Support:**
- https://ai.google.dev/
- Community: https://discuss.ai.google.dev/

---

**🎉 Enjoy your AI-powered health insights!**

*Last Updated: November 26, 2025*
