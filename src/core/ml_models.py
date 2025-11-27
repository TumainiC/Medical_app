"""
AI Model for Health Anomaly Detection
Implements machine learning models for detecting abnormal health conditions
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    classification_report, confusion_matrix, 
    accuracy_score, precision_score, recall_score, f1_score
)
import pickle
import joblib
from datetime import datetime
import json


class HealthAnomalyDetector:
    """Detects anomalies in health data using Isolation Forest"""
    
    def __init__(self, contamination=0.05, random_state=42):
        """
        Initialize anomaly detector
        
        Parameters:
        - contamination: Expected proportion of anomalies (default: 5%)
        - random_state: Random seed for reproducibility
        """
        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
            n_estimators=100,
            max_samples='auto',
            max_features=1.0
        )
        self.is_fitted = False
        self.feature_importance = None
        self.contamination = contamination
    
    def fit(self, X):
        """
        Train the anomaly detection model
        
        Parameters:
        - X: Feature matrix (preprocessed data)
        """
        self.model.fit(X)
        self.is_fitted = True
        
        # Calculate feature importance (approximate)
        self.feature_importance = self._calculate_feature_importance(X)
        
        return self
    
    def predict(self, X):
        """
        Predict anomalies
        
        Returns:
        - Array of predictions: -1 for anomaly, 1 for normal
        """
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call fit() first.")
        
        return self.model.predict(X)
    
    def predict_with_scores(self, X):
        """
        Predict anomalies with anomaly scores
        
        Returns:
        - predictions: Array of predictions (-1 or 1)
        - scores: Anomaly scores (lower = more anomalous)
        """
        predictions = self.predict(X)
        scores = self.model.score_samples(X)
        
        return predictions, scores
    
    def get_anomaly_labels(self, predictions):
        """Convert model predictions to readable labels"""
        return ['Anomaly' if p == -1 else 'Normal' for p in predictions]
    
    def _calculate_feature_importance(self, X):
        """Approximate feature importance based on average path length"""
        if isinstance(X, pd.DataFrame):
            feature_names = X.columns.tolist()
        else:
            feature_names = [f"feature_{i}" for i in range(X.shape[1])]
        
        # Simple importance calculation
        importances = np.abs(X.std(axis=0))
        importances = importances / importances.sum()
        
        return dict(zip(feature_names, importances))
    
    def save_model(self, filepath='models/anomaly_detector.pkl'):
        """Save trained model to disk"""
        model_data = {
            'model': self.model,
            'is_fitted': self.is_fitted,
            'feature_importance': self.feature_importance,
            'contamination': self.contamination
        }
        joblib.dump(model_data, filepath)
    
    def load_model(self, filepath='models/anomaly_detector.pkl'):
        """Load trained model from disk"""
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.is_fitted = model_data['is_fitted']
        self.feature_importance = model_data['feature_importance']
        self.contamination = model_data['contamination']


class HealthRiskClassifier:
    """Classifies health risk levels using supervised learning"""
    
    def __init__(self, random_state=42):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=random_state,
            class_weight='balanced'
        )
        self.is_fitted = False
        self.feature_names = None
        self.risk_levels = ['Low Risk', 'Medium Risk', 'High Risk']
    
    def create_risk_labels(self, df):
        """
        Create risk labels based on health metrics
        
        Parameters:
        - df: DataFrame with health metrics
        
        Returns:
        - Risk labels (0: Low, 1: Medium, 2: High)
        """
        risk = []
        
        for _, row in df.iterrows():
            risk_score = 0
            
            # Heart rate risk
            if row['heart_rate'] < 50 or row['heart_rate'] > 120:
                risk_score += 2
            elif row['heart_rate'] < 60 or row['heart_rate'] > 100:
                risk_score += 1
            
            # Blood oxygen risk
            if row['blood_oxygen'] < 90:
                risk_score += 2
            elif row['blood_oxygen'] < 95:
                risk_score += 1
            
            # Temperature risk
            if row['temperature'] < 35.5 or row['temperature'] > 38.0:
                risk_score += 2
            elif row['temperature'] < 36.1 or row['temperature'] > 37.5:
                risk_score += 1
            
            # Classify risk level
            if risk_score >= 4:
                risk.append(2)  # High Risk
            elif risk_score >= 2:
                risk.append(1)  # Medium Risk
            else:
                risk.append(0)  # Low Risk
        
        return np.array(risk)
    
    def fit(self, X, y):
        """Train the risk classifier"""
        if isinstance(X, pd.DataFrame):
            self.feature_names = X.columns.tolist()
        
        self.model.fit(X, y)
        self.is_fitted = True
        return self
    
    def predict(self, X):
        """Predict risk levels"""
        if not self.is_fitted:
            raise ValueError("Model not fitted. Call fit() first.")
        
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """Get probability estimates for each risk level"""
        return self.model.predict_proba(X)
    
    def get_feature_importance(self):
        """Get feature importance scores"""
        if not self.is_fitted:
            return None
        
        importances = self.model.feature_importances_
        if self.feature_names:
            return dict(zip(self.feature_names, importances))
        return importances
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance"""
        y_pred = self.predict(X_test)
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted'),
            'recall': recall_score(y_test, y_pred, average='weighted'),
            'f1_score': f1_score(y_test, y_pred, average='weighted'),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'classification_report': classification_report(
                y_test, y_pred, 
                target_names=self.risk_levels,
                output_dict=True
            )
        }
        
        return metrics
    
    def save_model(self, filepath='models/risk_classifier.pkl'):
        """Save trained model to disk"""
        model_data = {
            'model': self.model,
            'is_fitted': self.is_fitted,
            'feature_names': self.feature_names,
            'risk_levels': self.risk_levels
        }
        joblib.dump(model_data, filepath)
    
    def load_model(self, filepath='models/risk_classifier.pkl'):
        """Load trained model from disk"""
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.is_fitted = model_data['is_fitted']
        self.feature_names = model_data['feature_names']
        self.risk_levels = model_data['risk_levels']


class HealthRecommendationEngine:
    """Generates personalized health recommendations based on data analysis"""
    
    @staticmethod
    def generate_recommendations(health_data, anomaly_status, risk_level):
        """
        Generate personalized health recommendations
        
        Parameters:
        - health_data: Dict with current health metrics
        - anomaly_status: 'Anomaly' or 'Normal'
        - risk_level: 'Low Risk', 'Medium Risk', or 'High Risk'
        
        Returns:
        - List of recommendation strings
        """
        recommendations = []
        
        # Heart rate recommendations
        hr = health_data.get('heart_rate', 0)
        if hr < 60:
            recommendations.append("⚠️ Your heart rate is low. Consider consulting a healthcare provider if this persists.")
            recommendations.append("💡 Avoid sudden strenuous activities.")
        elif hr > 100:
            recommendations.append("⚠️ Your heart rate is elevated. Try relaxation techniques like deep breathing.")
            recommendations.append("💡 Reduce caffeine intake and ensure adequate hydration.")
        
        # Blood oxygen recommendations
        spo2 = health_data.get('blood_oxygen', 100)
        if spo2 < 95:
            recommendations.append("⚠️ Blood oxygen is below normal. Ensure good ventilation and avoid strenuous activities.")
            if spo2 < 90:
                recommendations.append("🚨 URGENT: Seek immediate medical attention - oxygen levels critically low!")
        
        # Temperature recommendations
        temp = health_data.get('temperature', 36.5)
        if temp > 37.5:
            recommendations.append("⚠️ Elevated temperature detected. Stay hydrated and monitor closely.")
            if temp > 38.0:
                recommendations.append("🚨 Fever detected. Consider taking fever-reducing medication and consult a doctor.")
        elif temp < 36.0:
            recommendations.append("⚠️ Body temperature is low. Warm up and monitor for hypothermia symptoms.")
        
        # Activity recommendations
        activity = health_data.get('activity_level', 'moderate')
        if activity == 'low':
            recommendations.append("💪 Try to increase physical activity gradually - aim for 30 minutes daily.")
        elif activity == 'high' and risk_level in ['Medium Risk', 'High Risk']:
            recommendations.append("⚠️ Consider moderating intense activity given your current health metrics.")
        
        # General recommendations based on risk level
        if risk_level == 'High Risk':
            recommendations.append("🚨 HIGH RISK ALERT: Schedule an immediate consultation with your healthcare provider.")
            recommendations.append("📱 Consider emergency services if symptoms worsen.")
        elif risk_level == 'Medium Risk':
            recommendations.append("⚠️ Schedule a check-up with your healthcare provider within 24-48 hours.")
            recommendations.append("📊 Continue monitoring your vitals closely.")
        else:
            recommendations.append("✅ Your vitals look good! Maintain healthy lifestyle habits.")
            recommendations.append("💧 Stay hydrated and get adequate rest.")
        
        # Anomaly-specific recommendations
        if anomaly_status == 'Anomaly':
            recommendations.append("⚠️ Unusual pattern detected in your health data. Monitor closely and consult a doctor if concerned.")
        
        return recommendations


if __name__ == "__main__":
    # Demo usage
    print("=== Health Anomaly Detection Demo ===\n")
    
    # Generate sample data
    from health_data import HealthDataSimulator, HealthDataPreprocessor
    
    simulator = HealthDataSimulator()
    df = simulator.generate_user_data("demo_user", num_records=100)
    
    preprocessor = HealthDataPreprocessor()
    df_encoded, df_scaled = preprocessor.fit_transform(df)
    
    # Train anomaly detector
    detector = HealthAnomalyDetector(contamination=0.1)
    detector.fit(df_scaled)
    
    predictions, scores = detector.predict_with_scores(df_scaled)
    labels = detector.get_anomaly_labels(predictions)
    
    print(f"Detected {sum([1 for l in labels if l == 'Anomaly'])} anomalies out of {len(labels)} records")
    print(f"\nFeature Importance: {detector.feature_importance}")
    
    # Train risk classifier
    print("\n=== Health Risk Classification Demo ===\n")
    classifier = HealthRiskClassifier()
    risk_labels = classifier.create_risk_labels(df_encoded)
    
    X_train, X_test, y_train, y_test = train_test_split(
        df_scaled, risk_labels, test_size=0.2, random_state=42
    )
    
    classifier.fit(X_train, y_train)
    metrics = classifier.evaluate(X_test, y_test)
    
    print(f"Model Accuracy: {metrics['accuracy']:.3f}")
    print(f"F1 Score: {metrics['f1_score']:.3f}")
