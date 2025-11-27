# 🏥 AI Health Monitoring System - Project Structure

## 📁 Directory Organization

```
Medical_app/
├── 📄 app.py                    # Main Flask application (entry point)
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env.template            # Environment variables template
├── 📄 .gitignore               # Git ignore rules
├── 📄 Dockerfile               # Docker configuration
├── 📄 setup.py                 # Package setup configuration
│
├── 📂 src/                     # Source code
│   ├── 📂 core/                # Core business logic
│   │   ├── __init__.py         # Package initialization
│   │   ├── health_data.py      # Data simulation & preprocessing
│   │   └── ml_models.py        # ML models (anomaly detection, risk classification)
│   │
│   ├── 📂 ai/                  # AI integration
│   │   ├── __init__.py         # Package initialization
│   │   └── gemini_advisor.py   # Gemini AI integration
│   │
│   └── 📂 utils/               # Utility functions
│       └── __init__.py         # Package initialization
│
├── 📂 tests/                   # Test files
│   ├── test_api.py             # API endpoint tests
│   ├── test_streaming.py       # Streaming functionality tests
│   ├── quick_test.py           # Quick smoke tests
│   └── verify_gemini.py        # Gemini integration verification
│
├── 📂 scripts/                 # Utility scripts
│   ├── train_models.py         # Model training script
│   └── cleanup_models.py       # Model cleanup utility
│
├── 📂 templates/               # HTML templates
│   └── index.html              # Main dashboard UI
│
├── 📂 static/                  # Static files (CSS, JS, images)
│   └── charts/                 # Generated chart images
│
├── 📂 models/                  # Trained ML models (generated)
│   ├── anomaly_detector.pkl    # Anomaly detection model
│   ├── risk_classifier.pkl     # Risk classification model
│   └── scaler.pkl              # Data scaler
│
└── 📂 docs/                    # Documentation
    ├── README.md               # Main documentation
    ├── API_DOCUMENTATION.md    # API reference
    ├── QUICK_START.md          # Quick start guide
    ├── GEMINI_SETUP.md         # Gemini integration guide
    ├── STREAMING_IMPLEMENTATION.md  # Streaming feature docs
    ├── VISUAL_COMPARISON.md    # UI before/after comparison
    └── PROJECT_SUMMARY.md      # Project overview
```

---

## 📦 Package Structure

### `src/core/` - Core Business Logic

**Purpose**: Contains the fundamental health monitoring functionality

**Modules**:
- `health_data.py`: Data simulation and preprocessing
  - `HealthDataSimulator`: Generate synthetic health data
  - `HealthDataPreprocessor`: Transform and scale data
  - `calculate_health_score()`: Calculate overall health score

- `ml_models.py`: Machine learning models
  - `HealthAnomalyDetector`: Isolation Forest for anomaly detection
  - `HealthRiskClassifier`: Random Forest for risk classification
  - `HealthRecommendationEngine`: Rule-based recommendations

**Import Example**:
```python
from src.core import (
    HealthDataSimulator,
    HealthAnomalyDetector,
    calculate_health_score
)
```

---

### `src/ai/` - AI Integration

**Purpose**: Gemini AI integration for intelligent health insights

**Modules**:
- `gemini_advisor.py`: Gemini Pro AI integration
  - `GeminiHealthAdvisor`: Main AI advisor class
  - Streaming support for real-time insights
  - Fallback to rule-based recommendations

**Import Example**:
```python
from src.ai import GeminiHealthAdvisor

advisor = GeminiHealthAdvisor()
insights = advisor.generate_comprehensive_insights(
    health_data=data,
    anomaly_status="Normal",
    risk_level="Low Risk"
)
```

---

### `src/utils/` - Utility Functions

**Purpose**: Helper functions and utilities

**Currently Empty** - Reserved for future utilities:
- Configuration helpers
- Logging utilities
- Data validation functions
- Common helpers

---

## 🧪 Tests Directory

### Purpose
Contains all test files for validating functionality

### Test Files

1. **`test_api.py`**: API endpoint testing
   ```bash
   python tests/test_api.py
   ```
   - Tests all REST API endpoints
   - Validates request/response formats
   - Checks error handling

2. **`test_streaming.py`**: Streaming functionality
   ```bash
   python tests/test_streaming.py
   ```
   - Tests Gemini streaming
   - Validates chunk generation
   - Checks response parsing

3. **`quick_test.py`**: Quick smoke tests
   ```bash
   python tests/quick_test.py
   ```
   - Fast verification of core features
   - Basic functionality checks

4. **`verify_gemini.py`**: Gemini integration
   ```bash
   python tests/verify_gemini.py
   ```
   - Verifies API key configuration
   - Tests Gemini connection
   - Validates AI responses

---

## 🔧 Scripts Directory

### Purpose
Utility scripts for development and maintenance

### Scripts

1. **`train_models.py`**: Train ML models
   ```bash
   python scripts/train_models.py
   ```
   - Trains anomaly detector
   - Trains risk classifier
   - Saves models to `models/` directory
   - Generates evaluation metrics

2. **`cleanup_models.py`**: Clean model files
   ```bash
   python scripts/cleanup_models.py
   ```
   - Removes old model files
   - Forces model retraining on next run
   - Useful for resolving model version conflicts

---

## 📚 Documentation Directory

### Purpose
All project documentation in one place

### Documents

- **README.md**: Main project documentation
- **API_DOCUMENTATION.md**: REST API reference
- **QUICK_START.md**: 5-minute setup guide
- **GEMINI_SETUP.md**: AI integration guide
- **STREAMING_IMPLEMENTATION.md**: Streaming feature details
- **VISUAL_COMPARISON.md**: UI improvements showcase
- **PROJECT_SUMMARY.md**: Project overview

---

## 🚀 Running the Application

### Development Mode

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Access at: http://localhost:5000

### Testing

```bash
# Run all tests
python tests/test_api.py
python tests/test_streaming.py
python tests/verify_gemini.py

# Quick smoke test
python tests/quick_test.py
```

### Training Models

```bash
# Train fresh models
python scripts/train_models.py

# Clean old models
python scripts/cleanup_models.py
```

---

## 🔄 Import Patterns

### From Main App (`app.py`)

```python
from src.core import (
    HealthDataSimulator,
    HealthDataPreprocessor,
    calculate_health_score,
    HealthAnomalyDetector,
    HealthRiskClassifier,
    HealthRecommendationEngine
)

from src.ai import GeminiHealthAdvisor
```

### From Test Files

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.core import HealthDataSimulator
from src.ai import GeminiHealthAdvisor
```

### From Scripts

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.core import HealthDataSimulator, HealthAnomalyDetector
```

---

## 📊 Data Flow

```
User Request
     ↓
app.py (Flask Routes)
     ↓
┌────────────────┬────────────────┬──────────────┐
│  src/core/     │   src/ai/      │  templates/  │
│  Data & ML     │   Gemini AI    │  HTML/JS     │
└────────────────┴────────────────┴──────────────┘
     ↓                  ↓                ↓
JSON Response    AI Insights      User Interface
```

---

## 🔧 Configuration

### Environment Variables

Create `.env` file from template:
```bash
cp .env.template .env
```

Required variables:
```bash
GEMINI_API_KEY=your_api_key_here
FLASK_SECRET_KEY=your_secret_key
FLASK_ENV=development
FLASK_DEBUG=True
```

### Models Directory

Generated automatically on first run:
```
models/
├── anomaly_detector.pkl   # Trained anomaly detection model
├── risk_classifier.pkl    # Trained risk classification model
└── scaler.pkl             # Data preprocessing scaler
```

---

## 🛠️ Development Workflow

1. **Make Code Changes**
   - Edit files in `src/` directory
   - Follow existing code patterns

2. **Test Changes**
   ```bash
   python tests/test_api.py
   python tests/quick_test.py
   ```

3. **Retrain Models** (if needed)
   ```bash
   python scripts/cleanup_models.py
   python scripts/train_models.py
   ```

4. **Run Application**
   ```bash
   python app.py
   ```

5. **Verify in Browser**
   - Open http://localhost:5000
   - Test functionality

---

## 📝 Adding New Features

### Adding a New Core Module

1. Create file in `src/core/`
2. Update `src/core/__init__.py`:
   ```python
   from .your_module import YourClass
   
   __all__ = [
       # ... existing exports
       'YourClass'
   ]
   ```

3. Import in `app.py`:
   ```python
   from src.core import YourClass
   ```

### Adding a New Test

1. Create file in `tests/`
2. Add path setup:
   ```python
   import sys
   import os
   sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
   ```

3. Import modules:
   ```python
   from src.core import ModuleToTest
   ```

### Adding Documentation

1. Create markdown file in `docs/`
2. Link from main README
3. Keep documentation up-to-date

---

## 🎯 Best Practices

### Code Organization

- ✅ Keep related functionality together
- ✅ Use clear, descriptive names
- ✅ Document complex functions
- ✅ Follow PEP 8 style guide

### Imports

- ✅ Use absolute imports from `src/`
- ✅ Import only what you need
- ✅ Group imports logically
- ✅ Avoid circular dependencies

### Testing

- ✅ Test after every change
- ✅ Write tests for new features
- ✅ Keep tests independent
- ✅ Use descriptive test names

### Documentation

- ✅ Update docs with code changes
- ✅ Add examples for complex features
- ✅ Keep README current
- ✅ Document API changes

---

## 🔍 Troubleshooting

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'src'`

**Solution**:
```python
# Add this at the top of your script
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
```

### Model Loading Errors

**Problem**: Model compatibility issues

**Solution**:
```bash
python scripts/cleanup_models.py
python scripts/train_models.py
```

### Gemini Not Available

**Problem**: AI features not working

**Solution**:
```bash
# Check if package is installed
pip show google-generativeai

# Install if missing
pip install -r requirements.txt

# Verify setup
python tests/verify_gemini.py
```

---

## 📦 Package Installation

### Development Install

```bash
# Install in editable mode
pip install -e .

# This allows:
from src.core import HealthDataSimulator
# To work from anywhere
```

### Production Install

```bash
pip install -r requirements.txt
```

---

## 🎓 Learning the Codebase

### Start Here

1. **Read**: `docs/README.md`
2. **Explore**: `src/core/health_data.py`
3. **Understand**: `src/core/ml_models.py`
4. **Review**: `app.py` Flask routes
5. **Examine**: `templates/index.html` UI
6. **Try**: `tests/quick_test.py`

### Key Concepts

1. **Data Flow**: User → Flask → ML Models → AI → Response
2. **Streaming**: Real-time AI insights via SSE
3. **Fallback**: Graceful degradation if AI fails
4. **Modular**: Separated concerns for maintainability

---

**Last Updated**: November 26, 2025

**Need Help?** Check `docs/` directory for comprehensive documentation!
