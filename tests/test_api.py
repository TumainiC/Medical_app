"""
API Testing Script for Health Monitoring System
Run this script to test all API endpoints
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:5000"
USER_ID = "test_user_001"

def print_response(response, endpoint_name):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"Testing: {endpoint_name}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))
    print(f"{'='*60}\n")

def test_simulate_data():
    """Test data simulation endpoint"""
    url = f"{BASE_URL}/api/health/simulate"
    payload = {
        "user_id": USER_ID,
        "num_records": 50
    }
    
    response = requests.post(url, json=payload)
    print_response(response, "Simulate Health Data")
    return response.status_code == 200

def test_analyze_data():
    """Test data analysis endpoint"""
    url = f"{BASE_URL}/api/health/analyze"
    payload = {
        "user_id": USER_ID
    }
    
    response = requests.post(url, json=payload)
    print_response(response, "Analyze Health Data")
    return response.status_code == 200

def test_realtime_analysis():
    """Test real-time analysis endpoint"""
    url = f"{BASE_URL}/api/health/realtime"
    payload = {
        "user_id": USER_ID,
        "heart_rate": 75,
        "blood_oxygen": 98,
        "temperature": 36.6,
        "respiration_rate": 16,
        "activity_level": "moderate",
        "steps": 50,
        "sleep_quality": "good"
    }
    
    response = requests.post(url, json=payload)
    print_response(response, "Real-time Health Analysis")
    return response.status_code == 200

def test_get_dashboard():
    """Test dashboard data endpoint"""
    url = f"{BASE_URL}/api/health/dashboard/{USER_ID}"
    
    response = requests.get(url)
    print_response(response, "Get Dashboard Data")
    return response.status_code == 200

def test_get_history():
    """Test user history endpoint"""
    url = f"{BASE_URL}/api/health/history/{USER_ID}?limit=20"
    
    response = requests.get(url)
    print_response(response, "Get User History")
    return response.status_code == 200

def test_get_statistics():
    """Test statistics endpoint"""
    url = f"{BASE_URL}/api/health/statistics/{USER_ID}"
    
    response = requests.get(url)
    print_response(response, "Get User Statistics")
    return response.status_code == 200

def test_model_info():
    """Test model information endpoint"""
    url = f"{BASE_URL}/api/model/info"
    
    response = requests.get(url)
    print_response(response, "Get Model Information")
    return response.status_code == 200

def test_export_data():
    """Test data export endpoint"""
    url = f"{BASE_URL}/api/health/export/{USER_ID}"
    
    response = requests.get(url)
    print(f"\n{'='*60}")
    print("Testing: Export User Data")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        filename = f"{USER_ID}_export.csv"
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"✓ Data exported successfully to {filename}")
    else:
        print(f"✗ Export failed")
    
    print(f"{'='*60}\n")
    return response.status_code == 200

def run_all_tests():
    """Run all API tests"""
    print("\n" + "="*60)
    print("🏥 HEALTH MONITORING SYSTEM - API TEST SUITE")
    print("="*60)
    print(f"\nBase URL: {BASE_URL}")
    print(f"Test User ID: {USER_ID}")
    print("\nStarting tests...\n")
    
    results = {}
    
    # Test sequence
    tests = [
        ("Simulate Data", test_simulate_data),
        ("Analyze Data", test_analyze_data),
        ("Real-time Analysis", test_realtime_analysis),
        ("Get Dashboard", test_get_dashboard),
        ("Get History", test_get_history),
        ("Get Statistics", test_get_statistics),
        ("Model Info", test_model_info),
        ("Export Data", test_export_data)
    ]
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
            time.sleep(0.5)  # Brief pause between tests
        except Exception as e:
            print(f"✗ {test_name} failed with error: {str(e)}")
            results[test_name] = False
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name:30} {status}")
    
    print(f"\n{passed}/{total} tests passed")
    print("="*60 + "\n")
    
    return passed == total

if __name__ == "__main__":
    print("\n⚠️  Make sure the Flask server is running on http://localhost:5000")
    input("Press Enter to start tests...")
    
    success = run_all_tests()
    
    if success:
        print("✓ All tests passed successfully!")
    else:
        print("✗ Some tests failed. Check the output above for details.")
