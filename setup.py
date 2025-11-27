#!/usr/bin/env python3
"""
Setup and Installation Script for Health Monitoring System
Run this script to set up the application for first use
"""

import os
import sys
import subprocess
import platform

def print_banner():
    """Print welcome banner"""
    print("\n" + "="*70)
    print("🏥 AI-Powered Health Monitoring System - Setup")
    print("="*70 + "\n")

def check_python_version():
    """Check if Python version is adequate"""
    print("📌 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_pip():
    """Check if pip is installed"""
    print("\n📌 Checking pip...")
    try:
        import pip
        print(f"✓ pip is installed")
        return True
    except ImportError:
        print("❌ pip is not installed!")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📌 Creating directories...")
    directories = ['models', 'static/charts', 'templates', 'evaluation_results']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created {directory}/")
    
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("\n📌 Installing dependencies...")
    print("This may take a few minutes...\n")
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ])
        print("\n✓ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("\n❌ Failed to install dependencies")
        return False

def train_initial_models():
    """Train ML models for first time"""
    print("\n📌 Training machine learning models...")
    print("This will take a few moments...\n")
    
    try:
        subprocess.check_call([sys.executable, 'train_models.py'])
        print("\n✓ Models trained successfully")
        return True
    except subprocess.CalledProcessError:
        print("\n⚠️  Model training failed, but you can train them later")
        print("   Run: python train_models.py")
        return True
    except FileNotFoundError:
        print("\n⚠️  train_models.py not found, skipping model training")
        return True

def create_env_file():
    """Create .env file for configuration"""
    print("\n📌 Creating environment configuration...")
    
    if os.path.exists('.env'):
        print("⚠️  .env file already exists, skipping")
        return True
    
    env_content = """# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-in-production

# Server Configuration
HOST=0.0.0.0
PORT=5000

# Model Configuration
ANOMALY_CONTAMINATION=0.05
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✓ Created .env file")
        return True
    except Exception as e:
        print(f"⚠️  Could not create .env file: {e}")
        return True

def verify_files():
    """Verify that required files exist"""
    print("\n📌 Verifying project files...")
    
    required_files = [
        'app.py',
        'health_data.py',
        'ml_models.py',
        'requirements.txt',
        'templates/index.html'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"❌ {file} - MISSING")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Warning: {len(missing_files)} required file(s) missing")
        return False
    
    return True

def print_next_steps():
    """Print instructions for next steps"""
    print("\n" + "="*70)
    print("✅ SETUP COMPLETE!")
    print("="*70)
    
    print("\n🚀 Quick Start:")
    print("\n1. Start the application:")
    print("   python app.py")
    
    print("\n2. Open your browser:")
    print("   http://localhost:5000")
    
    print("\n3. Try the Streamlit version (optional):")
    print("   streamlit run index.py")
    
    print("\n📚 Additional Resources:")
    print("   - README.md         - Full documentation")
    print("   - QUICKSTART.md     - Quick start guide")
    print("   - API_DOCUMENTATION.md - API reference")
    
    print("\n🧪 Testing:")
    print("   - python test_api.py    - Test all API endpoints")
    print("   - python train_models.py - Retrain ML models")
    
    print("\n" + "="*70)
    print("Happy monitoring! 🎉")
    print("="*70 + "\n")

def run_setup():
    """Run the complete setup process"""
    print_banner()
    
    steps = [
        ("Python Version", check_python_version),
        ("pip Installation", check_pip),
        ("Directory Structure", create_directories),
        ("File Verification", verify_files),
        ("Environment Config", create_env_file),
        ("Python Dependencies", install_dependencies),
        ("ML Models Training", train_initial_models)
    ]
    
    failed_steps = []
    
    for step_name, step_func in steps:
        try:
            if not step_func():
                failed_steps.append(step_name)
        except Exception as e:
            print(f"\n❌ Error in {step_name}: {str(e)}")
            failed_steps.append(step_name)
    
    if failed_steps:
        print("\n⚠️  Setup completed with warnings:")
        for step in failed_steps:
            print(f"   - {step}")
        print("\nYou may need to resolve these issues manually.")
    
    print_next_steps()
    
    return len(failed_steps) == 0

if __name__ == "__main__":
    try:
        success = run_setup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Setup failed with error: {str(e)}")
        sys.exit(1)
