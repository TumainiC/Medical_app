"""
Train and Evaluate Machine Learning Models
This script trains the models and provides detailed evaluation metrics
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.core import HealthDataSimulator, HealthDataPreprocessor
from src.core import HealthAnomalyDetector, HealthRiskClassifier

# Create output directory
os.makedirs('evaluation_results', exist_ok=True)
os.makedirs('models', exist_ok=True)

def train_and_evaluate_models():
    """Train both models and evaluate their performance"""
    
    print("="*70)
    print("🤖 TRAINING AND EVALUATING MACHINE LEARNING MODELS")
    print("="*70)
    
    # Step 1: Generate Training Data
    print("\n📊 Step 1: Generating training data...")
    simulator = HealthDataSimulator(seed=42)
    df_train = simulator.generate_multi_user_data(num_users=20, records_per_user=200)
    print(f"✓ Generated {len(df_train)} training records")
    
    # Step 2: Preprocess Data
    print("\n🔧 Step 2: Preprocessing data...")
    preprocessor = HealthDataPreprocessor()
    df_encoded, df_scaled = preprocessor.fit_transform(df_train)
    print("✓ Data preprocessed and scaled")
    
    # Save preprocessor
    preprocessor.save_scaler('models/scaler.pkl')
    print("✓ Scaler saved")
    
    # Step 3: Train Anomaly Detector
    print("\n🎯 Step 3: Training Anomaly Detector...")
    print("Algorithm: Isolation Forest")
    
    anomaly_detector = HealthAnomalyDetector(contamination=0.05, random_state=42)
    anomaly_detector.fit(df_scaled)
    
    # Predict on training data
    predictions, scores = anomaly_detector.predict_with_scores(df_scaled)
    anomaly_labels = anomaly_detector.get_anomaly_labels(predictions)
    
    num_anomalies = sum(1 for label in anomaly_labels if label == 'Anomaly')
    anomaly_rate = (num_anomalies / len(anomaly_labels)) * 100
    
    print(f"✓ Model trained")
    print(f"  - Detected {num_anomalies} anomalies ({anomaly_rate:.2f}%)")
    print(f"  - Feature Importance: {anomaly_detector.feature_importance}")
    
    # Save anomaly detector
    anomaly_detector.save_model('models/anomaly_detector.pkl')
    print("✓ Anomaly detector saved")
    
    # Step 4: Train Risk Classifier
    print("\n🎯 Step 4: Training Risk Classifier...")
    print("Algorithm: Random Forest Classifier")
    
    risk_classifier = HealthRiskClassifier(random_state=42)
    
    # Create risk labels
    risk_labels = risk_classifier.create_risk_labels(df_encoded)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        df_scaled, risk_labels, test_size=0.2, random_state=42, stratify=risk_labels
    )
    
    # Train model
    risk_classifier.fit(X_train, y_train)
    
    # Evaluate on test set
    metrics = risk_classifier.evaluate(X_test, y_test)
    
    print(f"✓ Model trained and evaluated")
    print(f"\n📈 Performance Metrics:")
    print(f"  - Accuracy:  {metrics['accuracy']:.4f}")
    print(f"  - Precision: {metrics['precision']:.4f}")
    print(f"  - Recall:    {metrics['recall']:.4f}")
    print(f"  - F1 Score:  {metrics['f1_score']:.4f}")
    
    # Cross-validation
    print("\n🔄 Performing cross-validation...")
    cv_scores = cross_val_score(risk_classifier.model, df_scaled, risk_labels, cv=5)
    print(f"✓ Cross-validation scores: {cv_scores}")
    print(f"  - Mean CV Score: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
    # Save risk classifier
    risk_classifier.save_model('models/risk_classifier.pkl')
    print("✓ Risk classifier saved")
    
    # Step 5: Visualizations
    print("\n📊 Step 5: Generating visualizations...")
    
    # Confusion Matrix
    plt.figure(figsize=(10, 8))
    cm = np.array(metrics['confusion_matrix'])
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=risk_classifier.risk_levels,
                yticklabels=risk_classifier.risk_levels)
    plt.title('Risk Classification - Confusion Matrix', fontsize=16, fontweight='bold')
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.tight_layout()
    plt.savefig('evaluation_results/confusion_matrix.png', dpi=300, bbox_inches='tight')
    print("✓ Confusion matrix saved")
    
    # Feature Importance
    plt.figure(figsize=(12, 6))
    feature_importance = risk_classifier.get_feature_importance()
    features = list(feature_importance.keys())
    importances = list(feature_importance.values())
    
    plt.bar(features, importances, color='skyblue', edgecolor='navy')
    plt.title('Feature Importance - Risk Classifier', fontsize=16, fontweight='bold')
    plt.xlabel('Features', fontsize=12)
    plt.ylabel('Importance', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('evaluation_results/feature_importance.png', dpi=300, bbox_inches='tight')
    print("✓ Feature importance chart saved")
    
    # Risk Distribution
    plt.figure(figsize=(10, 6))
    risk_counts = pd.Series(risk_labels).value_counts()
    risk_names = [risk_classifier.risk_levels[i] for i in risk_counts.index]
    colors = ['#28a745', '#ffc107', '#dc3545']
    
    plt.bar(risk_names, risk_counts.values, color=colors, edgecolor='black')
    plt.title('Risk Level Distribution in Training Data', fontsize=16, fontweight='bold')
    plt.xlabel('Risk Level', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.tight_layout()
    plt.savefig('evaluation_results/risk_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Risk distribution chart saved")
    
    # Classification Report
    print("\n📋 Detailed Classification Report:")
    print("-" * 70)
    for risk_level, metrics_data in metrics['classification_report'].items():
        if isinstance(metrics_data, dict):
            print(f"\n{risk_level}:")
            for metric, value in metrics_data.items():
                if metric != 'support':
                    print(f"  {metric}: {value:.4f}")
                else:
                    print(f"  {metric}: {int(value)}")
    
    # Step 6: Test with new data
    print("\n🧪 Step 6: Testing with new data...")
    df_test = simulator.generate_user_data("test_user", num_records=50)
    df_test_encoded, df_test_scaled = preprocessor.transform(df_test)
    
    # Anomaly detection
    test_predictions = anomaly_detector.predict(df_test_scaled)
    test_anomaly_labels = anomaly_detector.get_anomaly_labels(test_predictions)
    num_test_anomalies = sum(1 for label in test_anomaly_labels if label == 'Anomaly')
    
    # Risk classification
    test_risk_predictions = risk_classifier.predict(df_test_scaled)
    test_risk_labels = [risk_classifier.risk_levels[r] for r in test_risk_predictions]
    
    print(f"✓ Test results:")
    print(f"  - Anomalies detected: {num_test_anomalies}/{len(df_test)} ({num_test_anomalies/len(df_test)*100:.1f}%)")
    print(f"  - Risk distribution:")
    for risk_level in risk_classifier.risk_levels:
        count = test_risk_labels.count(risk_level)
        print(f"    {risk_level}: {count} ({count/len(test_risk_labels)*100:.1f}%)")
    
    # Save test results
    df_test_encoded['anomaly_status'] = test_anomaly_labels
    df_test_encoded['risk_level'] = test_risk_labels
    df_test_encoded.to_csv('evaluation_results/test_results.csv', index=False)
    print("\n✓ Test results saved to evaluation_results/test_results.csv")
    
    print("\n" + "="*70)
    print("✅ TRAINING AND EVALUATION COMPLETE")
    print("="*70)
    print("\nFiles saved:")
    print("  - models/anomaly_detector.pkl")
    print("  - models/risk_classifier.pkl")
    print("  - models/scaler.pkl")
    print("  - evaluation_results/confusion_matrix.png")
    print("  - evaluation_results/feature_importance.png")
    print("  - evaluation_results/risk_distribution.png")
    print("  - evaluation_results/test_results.csv")
    print("\n" + "="*70)

if __name__ == "__main__":
    train_and_evaluate_models()
