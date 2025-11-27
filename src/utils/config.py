"""
Configuration file for Health Monitoring System
Modify these settings to customize the application
"""

import os

class Config:
    """Base configuration"""
    
    # Flask Settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Server Settings
    HOST = '0.0.0.0'
    PORT = 5000
    
    # Model Settings
    MODEL_DIR = 'models'
    ANOMALY_CONTAMINATION = 0.05  # 5% expected anomaly rate
    RANDOM_STATE = 42
    
    # Data Simulation Settings
    DEFAULT_NUM_RECORDS = 100
    DEFAULT_NUM_USERS = 5
    
    # Health Metric Ranges (for validation and scoring)
    HEART_RATE_NORMAL = (60, 100)
    HEART_RATE_WARNING = (50, 120)
    
    BLOOD_OXYGEN_NORMAL = (95, 100)
    BLOOD_OXYGEN_WARNING = (90, 95)
    
    TEMPERATURE_NORMAL = (36.1, 37.2)
    TEMPERATURE_WARNING = (35.5, 38.0)
    
    RESPIRATION_RATE_NORMAL = (12, 20)
    
    # API Settings
    ENABLE_CORS = True
    API_RATE_LIMIT = None  # Set to '100 per hour' for rate limiting
    
    # Export Settings
    EXPORT_FORMAT = 'csv'
    EXPORT_FILENAME_PATTERN = '{user_id}_health_data_{date}.csv'
    
    # Chart Settings
    CHART_DIR = 'static/charts'
    CHART_DPI = 300
    
    # Logging Settings
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Override with environment variables in production
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Stricter settings for production
    ENABLE_CORS = False  # Configure specific origins
    API_RATE_LIMIT = '100 per hour'


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    
    # Use different model directory for tests
    MODEL_DIR = 'test_models'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env='development'):
    """Get configuration based on environment"""
    return config.get(env, config['default'])
