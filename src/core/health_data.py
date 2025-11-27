"""
Health Data Simulation and Preprocessing Module
Handles data generation, cleaning, and normalization for health monitoring
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.preprocessing import StandardScaler
import pickle


class HealthDataSimulator:
    """Simulates health data from wearable devices"""
    
    def __init__(self, seed=42):
        np.random.seed(seed)
    
    def generate_user_data(self, user_id, num_records=100, start_time=None):
        """
        Generate simulated health data for a single user
        
        Parameters:
        - user_id: Unique identifier for the user
        - num_records: Number of data points to generate
        - start_time: Starting timestamp (defaults to now)
        
        Returns:
        - DataFrame with health metrics
        """
        if start_time is None:
            start_time = datetime.now()
        
        data = []
        current_time = start_time
        
        for i in range(num_records):
            # Simulate normal patterns with occasional anomalies
            is_anomaly = np.random.random() < 0.05  # 5% anomaly rate
            
            if is_anomaly:
                # Create anomalous readings
                heart_rate = np.random.choice([
                    np.random.randint(40, 50),   # Too low
                    np.random.randint(120, 160)  # Too high
                ])
                blood_oxygen = np.random.randint(85, 92)
                temperature = np.random.choice([
                    np.random.normal(35.0, 0.3),  # Too low
                    np.random.normal(38.5, 0.5)   # Fever
                ])
            else:
                # Normal readings
                heart_rate = np.random.randint(60, 100)
                blood_oxygen = np.random.randint(95, 100)
                temperature = np.random.normal(36.5, 0.3)
            
            record = {
                'user_id': user_id,
                'timestamp': current_time,
                'heart_rate': heart_rate,
                'blood_oxygen': blood_oxygen,
                'temperature': round(temperature, 1),
                'respiration_rate': np.random.randint(12, 20),
                'activity_level': np.random.choice(['low', 'moderate', 'high']),
                'steps': np.random.randint(0, 150),
                'sleep_quality': np.random.choice(['poor', 'fair', 'good', 'excellent'])
            }
            
            data.append(record)
            current_time += timedelta(minutes=5)
        
        return pd.DataFrame(data)
    
    def generate_multi_user_data(self, num_users=5, records_per_user=100):
        """Generate data for multiple users"""
        all_data = []
        
        for i in range(num_users):
            user_id = f"user_{i+1:03d}"
            user_data = self.generate_user_data(user_id, records_per_user)
            all_data.append(user_data)
        
        return pd.concat(all_data, ignore_index=True)


class HealthDataPreprocessor:
    """Preprocesses health data for model training and inference"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_columns = [
            'heart_rate', 'blood_oxygen', 'temperature', 
            'respiration_rate', 'activity_level_encoded', 'steps'
        ]
        self.is_fitted = False
    
    def encode_categorical(self, df):
        """Encode categorical variables"""
        df = df.copy()
        
        # Encode activity level
        activity_map = {'low': 0, 'moderate': 1, 'high': 2}
        df['activity_level_encoded'] = df['activity_level'].map(activity_map)
        
        # Encode sleep quality
        sleep_map = {'poor': 0, 'fair': 1, 'good': 2, 'excellent': 3}
        df['sleep_quality_encoded'] = df['sleep_quality'].map(sleep_map)
        
        return df
    
    def fit_transform(self, df):
        """Fit scaler and transform data"""
        df_encoded = self.encode_categorical(df)
        
        # Select features for scaling
        X = df_encoded[self.feature_columns]
        
        # Fit and transform
        X_scaled = self.scaler.fit_transform(X)
        self.is_fitted = True
        
        # Create DataFrame with scaled features
        df_scaled = pd.DataFrame(
            X_scaled, 
            columns=self.feature_columns,
            index=df.index
        )
        
        return df_encoded, df_scaled
    
    def transform(self, df):
        """Transform data using fitted scaler"""
        if not self.is_fitted:
            raise ValueError("Preprocessor not fitted. Call fit_transform first.")
        
        df_encoded = self.encode_categorical(df)
        X = df_encoded[self.feature_columns]
        X_scaled = self.scaler.transform(X)
        
        df_scaled = pd.DataFrame(
            X_scaled,
            columns=self.feature_columns,
            index=df.index
        )
        
        return df_encoded, df_scaled
    
    def save_scaler(self, filepath='models/scaler.pkl'):
        """Save fitted scaler to disk"""
        with open(filepath, 'wb') as f:
            pickle.dump(self.scaler, f)
    
    def load_scaler(self, filepath='models/scaler.pkl'):
        """Load fitted scaler from disk"""
        with open(filepath, 'rb') as f:
            self.scaler = pickle.load(f)
        self.is_fitted = True


def calculate_health_score(row):
    """Calculate overall health score based on metrics"""
    score = 100
    
    # Heart rate scoring
    if 60 <= row['heart_rate'] <= 100:
        score += 0
    elif 50 <= row['heart_rate'] < 60 or 100 < row['heart_rate'] <= 120:
        score -= 10
    else:
        score -= 25
    
    # Blood oxygen scoring
    if row['blood_oxygen'] >= 95:
        score += 0
    elif 90 <= row['blood_oxygen'] < 95:
        score -= 15
    else:
        score -= 30
    
    # Temperature scoring
    if 36.1 <= row['temperature'] <= 37.2:
        score += 0
    elif 35.5 <= row['temperature'] < 36.1 or 37.2 < row['temperature'] <= 38.0:
        score -= 10
    else:
        score -= 20
    
    return max(0, min(100, score))


if __name__ == "__main__":
    # Demo usage
    print("=== Health Data Simulator Demo ===\n")
    
    # Generate data
    simulator = HealthDataSimulator()
    df = simulator.generate_user_data("test_user", num_records=20)
    print("Generated Data Sample:")
    print(df.head())
    print(f"\nShape: {df.shape}")
    
    # Preprocess data
    print("\n=== Preprocessing Demo ===\n")
    preprocessor = HealthDataPreprocessor()
    df_encoded, df_scaled = preprocessor.fit_transform(df)
    print("Scaled Features Sample:")
    print(df_scaled.head())
