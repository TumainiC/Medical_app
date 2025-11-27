"""
Quick Test Script - Verify the application is working
Run this to test if the Flask server is responding correctly
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_server():
    """Test if server is running"""
    print("🔍 Testing Flask Server Connection...")
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            print("✓ Server is running and accessible")
            return True
        else:
            print(f"⚠️ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is the Flask app running?")
        print("   Run: python app.py")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_simulate_endpoint():
    """Test the simulate endpoint"""
    print("\n🧪 Testing /api/health/simulate endpoint...")
    try:
        payload = {
            "user_id": "test_user",
            "num_records": 10
        }
        
        response = requests.post(
            f"{BASE_URL}/api/health/simulate",
            json=payload,
            timeout=10
        )
        
        data = response.json()
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(data, indent=2)[:500]}...")
        
        if data.get('success'):
            print("✓ Simulate endpoint working correctly")
            return True
        else:
            print(f"⚠️ Endpoint returned success=false: {data.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing simulate endpoint: {str(e)}")
        return False

def test_dashboard_endpoint():
    """Test the dashboard endpoint"""
    print("\n🧪 Testing /api/health/dashboard endpoint...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/health/dashboard/test_user",
            timeout=10
        )
        
        data = response.json()
        print(f"Status Code: {response.status_code}")
        
        if data.get('success'):
            print("✓ Dashboard endpoint working correctly")
            print(f"  Health Score: {data['dashboard']['current_metrics']['health_score']}")
            print(f"  Anomaly Status: {data['dashboard']['status']['anomaly']}")
            print(f"  Risk Level: {data['dashboard']['status']['risk_level']}")
            return True
        else:
            print(f"⚠️ Endpoint returned success=false: {data.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing dashboard endpoint: {str(e)}")
        return False

def main():
    print("="*60)
    print("🏥 Health Monitoring System - Quick Test")
    print("="*60)
    
    # Test 1: Server connection
    if not test_server():
        print("\n⚠️ Server is not running. Please start it with: python app.py")
        return
    
    # Test 2: Simulate endpoint
    test_simulate_endpoint()
    
    # Test 3: Dashboard endpoint
    test_dashboard_endpoint()
    
    print("\n" + "="*60)
    print("🎉 Testing Complete!")
    print("="*60)
    print("\nIf all tests passed, open your browser to:")
    print("http://localhost:5000")
    print("\nThen:")
    print("1. Enter a user ID (e.g., user_001)")
    print("2. Click 'Load Dashboard'")
    print("3. Watch for toast notifications showing progress")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
