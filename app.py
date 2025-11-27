"""
Flask Web Application for AI-Powered Health Monitoring System
Provides REST APIs and web interface for health monitoring
"""

from flask import Flask, render_template, request, jsonify, Response, send_file
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import custom modules
from src.core import (
    HealthDataSimulator, 
    HealthDataPreprocessor, 
    calculate_health_score,
    HealthAnomalyDetector, 
    HealthRiskClassifier,
    HealthRecommendationEngine
)

# Try to import Gemini advisor
try:
    from src.ai import GeminiHealthAdvisor
    GEMINI_AVAILABLE = True
    logger.info("✓ Gemini AI module imported successfully")
except ImportError as e:
    GEMINI_AVAILABLE = False
    logger.warning(f"⚠️  Gemini AI not available: {str(e)}")
    logger.warning("   Install with: pip install google-generativeai python-dotenv")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for mobile app integration

# Configure app
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['JSON_SORT_KEYS'] = False

# Initialize models and data components
simulator = HealthDataSimulator()
preprocessor = HealthDataPreprocessor()
anomaly_detector = HealthAnomalyDetector(contamination=0.05)
risk_classifier = HealthRiskClassifier()
recommendation_engine = HealthRecommendationEngine()

# Initialize Gemini advisor if available
gemini_advisor = None
if GEMINI_AVAILABLE:
    try:
        gemini_advisor = GeminiHealthAdvisor()
        logger.info("✓ Gemini Health Advisor initialized")
    except Exception as e:
        logger.warning(f"⚠️  Could not initialize Gemini: {str(e)}")
        logger.warning("   Falling back to rule-based recommendations")
        GEMINI_AVAILABLE = False

# Global storage (in production, use a database)
user_data_store = {}
model_trained = False

# Create necessary directories
os.makedirs('models', exist_ok=True)
os.makedirs('static/charts', exist_ok=True)
os.makedirs('templates', exist_ok=True)


def initialize_models():
    """Initialize and train ML models with sample data"""
    global model_trained, preprocessor, anomaly_detector, risk_classifier
    
    try:
        # Try to load existing models
        logger.info("Attempting to load existing models...")
        anomaly_detector.load_model('models/anomaly_detector.pkl')
        risk_classifier.load_model('models/risk_classifier.pkl')
        preprocessor.load_scaler('models/scaler.pkl')
        model_trained = True
        logger.info("✓ Models loaded from disk")
    except Exception as e:
        # If loading fails, train new models
        logger.warning(f"Could not load models: {str(e)}")
        logger.info("Training new models...")
        
        try:
            # Generate training data
            train_df = simulator.generate_multi_user_data(num_users=10, records_per_user=200)
            df_encoded, df_scaled = preprocessor.fit_transform(train_df)
            
            # Train anomaly detector
            anomaly_detector.fit(df_scaled)
            
            # Train risk classifier
            risk_labels = risk_classifier.create_risk_labels(df_encoded)
            risk_classifier.fit(df_scaled, risk_labels)
            
            # Save models
            try:
                anomaly_detector.save_model('models/anomaly_detector.pkl')
                risk_classifier.save_model('models/risk_classifier.pkl')
                preprocessor.save_scaler('models/scaler.pkl')
                logger.info("✓ Models saved to disk")
            except Exception as save_error:
                logger.warning(f"Could not save models: {str(save_error)}")
            
            model_trained = True
            logger.info("✓ Models trained successfully")
        except Exception as train_error:
            logger.error(f"Failed to train models: {str(train_error)}")
            raise


@app.route('/')
def home():
    """Main dashboard page"""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """Modern React dashboard integrated with backend"""
    return render_template('dashboard.html')


@app.route('/api/health/simulate', methods=['POST'])
def simulate_health_data():
    """
    API endpoint to generate simulated health data
    
    POST body:
    {
        "user_id": "user_001",
        "num_records": 100
    }
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'demo_user')
        num_records = data.get('num_records', 100)
        
        # Generate data
        df = simulator.generate_user_data(user_id, num_records)
        
        # Store data
        user_data_store[user_id] = df
        
        # Convert to JSON-friendly format
        result = df.to_dict(orient='records')
        
        return jsonify({
            'success': True,
            'message': f'Generated {num_records} health records for {user_id}',
            'user_id': user_id,
            'num_records': len(result),
            'data': result[:10]  # Return first 10 records
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/health/analyze', methods=['POST'])
def analyze_health_data():
    """
    API endpoint to analyze health data and detect anomalies
    
    POST body:
    {
        "user_id": "user_001",
        "data": [...] or use stored data
    }
    """
    try:
        if not model_trained:
            initialize_models()
        
        data = request.get_json()
        user_id = data.get('user_id')
        
        # Get data from request or storage
        if 'data' in data:
            df = pd.DataFrame(data['data'])
        elif user_id in user_data_store:
            df = user_data_store[user_id]
        else:
            return jsonify({
                'success': False,
                'error': 'No data provided or found for user'
            }), 400
        
        # Preprocess data
        df_encoded, df_scaled = preprocessor.transform(df)
        
        # Detect anomalies
        predictions, scores = anomaly_detector.predict_with_scores(df_scaled)
        anomaly_labels = anomaly_detector.get_anomaly_labels(predictions)
        
        # Classify risk
        risk_predictions = risk_classifier.predict(df_scaled)
        risk_probabilities = risk_classifier.predict_proba(df_scaled)
        risk_labels = [risk_classifier.risk_levels[r] for r in risk_predictions]
        
        # Calculate health scores
        df_encoded['health_score'] = df_encoded.apply(calculate_health_score, axis=1)
        
        # Add predictions to dataframe
        df_encoded['anomaly_status'] = anomaly_labels
        df_encoded['risk_level'] = risk_labels
        df_encoded['anomaly_score'] = scores
        
        # Calculate statistics
        total_records = len(df_encoded)
        num_anomalies = sum([1 for l in anomaly_labels if l == 'Anomaly'])
        anomaly_rate = (num_anomalies / total_records) * 100
        
        avg_health_score = df_encoded['health_score'].mean()
        
        risk_distribution = df_encoded['risk_level'].value_counts().to_dict()
        
        # Get latest record for current status
        latest_record = df_encoded.iloc[-1]
        
        # Generate recommendations (use Gemini if available)
        if GEMINI_AVAILABLE and gemini_advisor:
            try:
                logger.info("🤖 Generating AI-powered insights with Gemini...")
                gemini_insights = gemini_advisor.generate_comprehensive_insights(
                    health_data=latest_record.to_dict(),
                    anomaly_status=latest_record['anomaly_status'],
                    risk_level=latest_record['risk_level'],
                    historical_trends={
                        'heart_rate': df_encoded['heart_rate'].tail(20).tolist(),
                        'blood_oxygen': df_encoded['blood_oxygen'].tail(20).tolist(),
                        'temperature': df_encoded['temperature'].tail(20).tolist()
                    }
                )
                current_recommendations = gemini_insights.get('recommendations', [])
                ai_insights = gemini_insights
                using_ai = True
            except Exception as e:
                logger.warning(f"⚠️  Gemini failed, using fallback: {str(e)}")
                current_recommendations = recommendation_engine.generate_recommendations(
                    latest_record.to_dict(),
                    latest_record['anomaly_status'],
                    latest_record['risk_level']
                )
                ai_insights = None
                using_ai = False
        else:
            current_recommendations = recommendation_engine.generate_recommendations(
                latest_record.to_dict(),
                latest_record['anomaly_status'],
                latest_record['risk_level']
            )
            ai_insights = None
            using_ai = False
        
        response_data = {
            'success': True,
            'user_id': user_id,
            'using_ai': using_ai,
            'analysis': {
                'total_records': total_records,
                'num_anomalies': num_anomalies,
                'anomaly_rate': round(anomaly_rate, 2),
                'avg_health_score': round(avg_health_score, 2),
                'risk_distribution': risk_distribution
            },
            'current_status': {
                'heart_rate': int(latest_record['heart_rate']),
                'blood_oxygen': int(latest_record['blood_oxygen']),
                'temperature': float(latest_record['temperature']),
                'health_score': int(latest_record['health_score']),
                'anomaly_status': latest_record['anomaly_status'],
                'risk_level': latest_record['risk_level'],
                'timestamp': str(latest_record['timestamp'])
            },
            'recommendations': current_recommendations,
            'detailed_results': df_encoded[['timestamp', 'heart_rate', 'blood_oxygen', 
                                           'temperature', 'anomaly_status', 'risk_level', 
                                           'health_score']].tail(20).to_dict(orient='records')
        }
        
        # Add AI insights if available
        if ai_insights:
            response_data['ai_insights'] = ai_insights
        
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health/realtime', methods=['POST'])
def analyze_realtime_data():
    """
    API endpoint for real-time single record analysis
    
    POST body:
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
    """
    try:
        if not model_trained:
            initialize_models()
        
        data = request.get_json()
        
        # Create DataFrame from single record
        record_data = {
            'user_id': data.get('user_id', 'unknown'),
            'timestamp': datetime.now(),
            'heart_rate': data.get('heart_rate'),
            'blood_oxygen': data.get('blood_oxygen'),
            'temperature': data.get('temperature'),
            'respiration_rate': data.get('respiration_rate'),
            'activity_level': data.get('activity_level', 'moderate'),
            'steps': data.get('steps', 0),
            'sleep_quality': data.get('sleep_quality', 'good')
        }
        
        df = pd.DataFrame([record_data])
        
        # Preprocess
        df_encoded, df_scaled = preprocessor.transform(df)
        
        # Predict
        prediction = anomaly_detector.predict(df_scaled)[0]
        anomaly_status = 'Anomaly' if prediction == -1 else 'Normal'
        anomaly_score = anomaly_detector.model.score_samples(df_scaled)[0]
        
        risk_pred = risk_classifier.predict(df_scaled)[0]
        risk_level = risk_classifier.risk_levels[risk_pred]
        risk_probs = risk_classifier.predict_proba(df_scaled)[0]
        
        health_score = calculate_health_score(df_encoded.iloc[0])
        
        # Generate recommendations (use Gemini if available)
        if GEMINI_AVAILABLE and gemini_advisor:
            try:
                logger.info("🤖 Generating real-time AI insights with Gemini...")
                record_data['health_score'] = int(health_score)
                gemini_insights = gemini_advisor.generate_comprehensive_insights(
                    health_data=record_data,
                    anomaly_status=anomaly_status,
                    risk_level=risk_level
                )
                recommendations = gemini_insights.get('recommendations', [])
                ai_insights = gemini_insights
                using_ai = True
            except Exception as e:
                logger.warning(f"⚠️  Gemini failed, using fallback: {str(e)}")
                recommendations = recommendation_engine.generate_recommendations(
                    record_data,
                    anomaly_status,
                    risk_level
                )
                ai_insights = None
                using_ai = False
        else:
            recommendations = recommendation_engine.generate_recommendations(
                record_data,
                anomaly_status,
                risk_level
            )
            ai_insights = None
            using_ai = False
        
        response_data = {
            'success': True,
            'using_ai': using_ai,
            'user_id': record_data['user_id'],
            'timestamp': str(record_data['timestamp']),
            'metrics': {
                'heart_rate': record_data['heart_rate'],
                'blood_oxygen': record_data['blood_oxygen'],
                'temperature': record_data['temperature'],
                'respiration_rate': record_data['respiration_rate'],
                'activity_level': record_data['activity_level']
            },
            'analysis': {
                'health_score': int(health_score),
                'anomaly_status': anomaly_status,
                'anomaly_score': float(anomaly_score),
                'risk_level': risk_level,
                'risk_probabilities': {
                    'low': float(risk_probs[0]),
                    'medium': float(risk_probs[1]),
                    'high': float(risk_probs[2])
                }
            },
            'recommendations': recommendations
        }
        
        # Add AI insights if available
        if ai_insights:
            response_data['ai_insights'] = ai_insights
        
        return jsonify(response_data)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/health/history/<user_id>', methods=['GET'])
def get_user_history(user_id):
    """Get historical health data for a user"""
    try:
        if user_id not in user_data_store:
            return jsonify({
                'success': False,
                'error': f'No data found for user {user_id}'
            }), 404
        
        df = user_data_store[user_id]
        
        # Get query parameters for filtering
        limit = request.args.get('limit', 100, type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Filter by date if provided
        if start_date:
            df = df[df['timestamp'] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df['timestamp'] <= pd.to_datetime(end_date)]
        
        # Limit results
        df = df.tail(limit)
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'num_records': len(df),
            'data': df.to_dict(orient='records')
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health/statistics/<user_id>', methods=['GET'])
def get_user_statistics(user_id):
    """Get statistical summary of user's health data"""
    try:
        if user_id not in user_data_store:
            return jsonify({
                'success': False,
                'error': f'No data found for user {user_id}'
            }), 404
        
        df = user_data_store[user_id]
        
        stats = {
            'heart_rate': {
                'mean': float(df['heart_rate'].mean()),
                'min': int(df['heart_rate'].min()),
                'max': int(df['heart_rate'].max()),
                'std': float(df['heart_rate'].std())
            },
            'blood_oxygen': {
                'mean': float(df['blood_oxygen'].mean()),
                'min': int(df['blood_oxygen'].min()),
                'max': int(df['blood_oxygen'].max()),
                'std': float(df['blood_oxygen'].std())
            },
            'temperature': {
                'mean': float(df['temperature'].mean()),
                'min': float(df['temperature'].min()),
                'max': float(df['temperature'].max()),
                'std': float(df['temperature'].std())
            },
            'activity_distribution': df['activity_level'].value_counts().to_dict(),
            'total_steps': int(df['steps'].sum()),
            'avg_steps_per_record': float(df['steps'].mean())
        }
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'statistics': stats
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health/export/<user_id>', methods=['GET'])
def export_user_data(user_id):
    """Export user data as CSV"""
    try:
        if user_id not in user_data_store:
            return jsonify({
                'success': False,
                'error': f'No data found for user {user_id}'
            }), 404
        
        df = user_data_store[user_id]
        
        # Create CSV in memory
        output = BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'{user_id}_health_data_{datetime.now().strftime("%Y%m%d")}.csv'
        )
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/model/info', methods=['GET'])
def get_model_info():
    """Get information about the ML models"""
    try:
        if not model_trained:
            return jsonify({
                'success': False,
                'error': 'Models not initialized'
            }), 400
        
        info = {
            'anomaly_detector': {
                'type': 'Isolation Forest',
                'contamination': anomaly_detector.contamination,
                'feature_importance': anomaly_detector.feature_importance
            },
            'risk_classifier': {
                'type': 'Random Forest Classifier',
                'risk_levels': risk_classifier.risk_levels,
                'feature_importance': risk_classifier.get_feature_importance()
            },
            'ai_advisor': {
                'available': GEMINI_AVAILABLE,
                'model': 'Google Gemini Pro' if GEMINI_AVAILABLE else 'Rule-based',
                'status': 'Active' if (GEMINI_AVAILABLE and gemini_advisor) else 'Inactive'
            }
        }
        
        return jsonify({
            'success': True,
            'models': info
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health/dashboard/<user_id>/stream', methods=['GET'])
def stream_dashboard_insights(user_id):
    """Stream AI insights for dashboard in real-time"""
    def generate():
        try:
            if not model_trained:
                initialize_models()
            
            # Generate or get data
            if user_id not in user_data_store:
                df = simulator.generate_user_data(user_id, num_records=100)
                user_data_store[user_id] = df
            else:
                df = user_data_store[user_id]
            
            # Analyze data
            df_encoded, df_scaled = preprocessor.transform(df)
            
            predictions, scores = anomaly_detector.predict_with_scores(df_scaled)
            anomaly_labels = anomaly_detector.get_anomaly_labels(predictions)
            
            risk_predictions = risk_classifier.predict(df_scaled)
            risk_labels = [risk_classifier.risk_levels[r] for r in risk_predictions]
            
            df_encoded['health_score'] = df_encoded.apply(calculate_health_score, axis=1)
            df_encoded['anomaly_status'] = anomaly_labels
            df_encoded['risk_level'] = risk_labels
            
            latest = df_encoded.iloc[-1]
            
            # Send initial data first
            initial_data = {
                'type': 'metrics',
                'data': {
                    'current_metrics': {
                        'heart_rate': int(latest['heart_rate']),
                        'blood_oxygen': int(latest['blood_oxygen']),
                        'temperature': float(latest['temperature']),
                        'respiration_rate': int(latest['respiration_rate']),
                        'health_score': int(latest['health_score'])
                    },
                    'status': {
                        'anomaly': latest['anomaly_status'],
                        'risk_level': latest['risk_level']
                    },
                    'statistics': {
                        'total_records': len(df_encoded),
                        'anomaly_count': sum([1 for l in anomaly_labels if l == 'Anomaly']),
                        'avg_health_score': float(df_encoded['health_score'].mean()),
                        'risk_distribution': df_encoded['risk_level'].value_counts().to_dict()
                    },
                    'trends': {
                        'heart_rate': df_encoded['heart_rate'].tail(20).tolist(),
                        'blood_oxygen': df_encoded['blood_oxygen'].tail(20).tolist(),
                        'temperature': df_encoded['temperature'].tail(20).tolist(),
                        'health_score': df_encoded['health_score'].tail(20).tolist(),
                        'timestamps': [str(t) for t in df_encoded['timestamp'].tail(20).tolist()]
                    }
                }
            }
            yield f"data: {json.dumps(initial_data)}\n\n"
            
            # Stream AI insights if available
            if GEMINI_AVAILABLE and gemini_advisor:
                try:
                    logger.info("🤖 Starting streaming dashboard insights with Gemini...")
                    yield f"data: {{\"type\": \"ai_start\", \"using_ai\": true}}\n\n"
                    
                    for chunk in gemini_advisor.generate_comprehensive_insights_stream(
                        health_data=latest.to_dict(),
                        anomaly_status=latest['anomaly_status'],
                        risk_level=latest['risk_level'],
                        historical_trends={
                            'heart_rate': df_encoded['heart_rate'].tail(20).tolist(),
                            'blood_oxygen': df_encoded['blood_oxygen'].tail(20).tolist(),
                            'temperature': df_encoded['temperature'].tail(20).tolist()
                        }
                    ):
                        chunk_data = {
                            'type': 'ai_chunk',
                            'chunk': chunk
                        }
                        yield f"data: {json.dumps(chunk_data)}\n\n"
                    
                    yield f"data: {{\"type\": \"ai_complete\"}}\n\n"
                    
                except AttributeError as e:
                    logger.error(f"⚠️  Model attribute error: {str(e)}")
                    # Fall back to rule-based
                    recommendations = recommendation_engine.generate_recommendations(
                        latest.to_dict(),
                        latest['anomaly_status'],
                        latest['risk_level']
                    )
                    fallback_data = {
                        'type': 'fallback',
                        'using_ai': False,
                        'recommendations': recommendations
                    }
                    yield f"data: {json.dumps(fallback_data)}\n\n"
                except Exception as e:
                    logger.warning(f"⚠️  Gemini streaming failed: {str(e)}")
                    # Fall back to rule-based
                    recommendations = recommendation_engine.generate_recommendations(
                        latest.to_dict(),
                        latest['anomaly_status'],
                        latest['risk_level']
                    )
                    fallback_data = {
                        'type': 'fallback',
                        'using_ai': False,
                        'recommendations': recommendations
                    }
                    yield f"data: {json.dumps(fallback_data)}\n\n"
            else:
                # Use rule-based recommendations
                recommendations = recommendation_engine.generate_recommendations(
                    latest.to_dict(),
                    latest['anomaly_status'],
                    latest['risk_level']
                )
                fallback_data = {
                    'type': 'fallback',
                    'using_ai': False,
                    'recommendations': recommendations
                }
                yield f"data: {json.dumps(fallback_data)}\n\n"
            
            yield f"data: {{\"type\": \"complete\"}}\n\n"
            
        except Exception as e:
            error_data = {
                'type': 'error',
                'error': str(e)
            }
            yield f"data: {json.dumps(error_data)}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')


@app.route('/api/health/dashboard/<user_id>', methods=['GET'])
def get_dashboard_data(user_id):
    """Get comprehensive dashboard data for a user"""
    try:
        if not model_trained:
            initialize_models()
        
        # Generate or get data
        if user_id not in user_data_store:
            df = simulator.generate_user_data(user_id, num_records=100)
            user_data_store[user_id] = df
        else:
            df = user_data_store[user_id]
        
        # Analyze data
        df_encoded, df_scaled = preprocessor.transform(df)
        
        predictions, scores = anomaly_detector.predict_with_scores(df_scaled)
        anomaly_labels = anomaly_detector.get_anomaly_labels(predictions)
        
        risk_predictions = risk_classifier.predict(df_scaled)
        risk_labels = [risk_classifier.risk_levels[r] for r in risk_predictions]
        
        df_encoded['health_score'] = df_encoded.apply(calculate_health_score, axis=1)
        df_encoded['anomaly_status'] = anomaly_labels
        df_encoded['risk_level'] = risk_labels
        
        # Prepare dashboard data
        latest = df_encoded.iloc[-1]
        
        # Generate recommendations (use Gemini if available)
        if GEMINI_AVAILABLE and gemini_advisor:
            try:
                logger.info("🤖 Generating dashboard insights with Gemini...")
                gemini_insights = gemini_advisor.generate_comprehensive_insights(
                    health_data=latest.to_dict(),
                    anomaly_status=latest['anomaly_status'],
                    risk_level=latest['risk_level'],
                    historical_trends={
                        'heart_rate': df_encoded['heart_rate'].tail(20).tolist(),
                        'blood_oxygen': df_encoded['blood_oxygen'].tail(20).tolist(),
                        'temperature': df_encoded['temperature'].tail(20).tolist()
                    }
                )
                recommendations = gemini_insights.get('recommendations', [])
                ai_insights_available = gemini_insights
                using_ai = True
            except Exception as e:
                logger.warning(f"⚠️  Gemini failed, using fallback: {str(e)}")
                recommendations = recommendation_engine.generate_recommendations(
                    latest.to_dict(),
                    latest['anomaly_status'],
                    latest['risk_level']
                )
                ai_insights_available = None
                using_ai = False
        else:
            recommendations = recommendation_engine.generate_recommendations(
                latest.to_dict(),
                latest['anomaly_status'],
                latest['risk_level']
            )
            ai_insights_available = None
            using_ai = False
        
        dashboard_data = {
            'user_id': user_id,
            'using_ai': using_ai,
            'last_updated': str(latest['timestamp']),
            'current_metrics': {
                'heart_rate': int(latest['heart_rate']),
                'blood_oxygen': int(latest['blood_oxygen']),
                'temperature': float(latest['temperature']),
                'respiration_rate': int(latest['respiration_rate']),
                'health_score': int(latest['health_score'])
            },
            'status': {
                'anomaly': latest['anomaly_status'],
                'risk_level': latest['risk_level']
            },
            'trends': {
                'heart_rate': df_encoded['heart_rate'].tail(20).tolist(),
                'blood_oxygen': df_encoded['blood_oxygen'].tail(20).tolist(),
                'temperature': df_encoded['temperature'].tail(20).tolist(),
                'health_score': df_encoded['health_score'].tail(20).tolist(),
                'timestamps': [str(t) for t in df_encoded['timestamp'].tail(20).tolist()]
            },
            'statistics': {
                'total_records': len(df_encoded),
                'anomaly_count': sum([1 for l in anomaly_labels if l == 'Anomaly']),
                'avg_health_score': float(df_encoded['health_score'].mean()),
                'risk_distribution': df_encoded['risk_level'].value_counts().to_dict()
            },
            'recommendations': recommendations
        }
        
        # Add AI insights if available
        if ai_insights_available:
            dashboard_data['ai_insights'] = ai_insights_available
        
        return jsonify({
            'success': True,
            'dashboard': dashboard_data
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🏥 AI-Powered Health Monitoring System")
    print("=" * 60)
    print("\nInitializing ML models...")
    initialize_models()
    print("\n✓ System ready!")
    print("\nStarting Flask server...")
    print("Access the application at: http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
