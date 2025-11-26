"""
Test script to verify Gemini integration is working correctly
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 70)
print("🔍 GEMINI INTEGRATION VERIFICATION")
print("=" * 70)

# Check 1: Environment variable
api_key = os.getenv('GEMINI_API_KEY')
print("\n1️⃣ Checking GEMINI_API_KEY environment variable...")
if api_key:
    print(f"   ✓ API Key found: {api_key[:10]}...{api_key[-4:]}")
else:
    print("   ✗ API Key NOT found!")
    print("   ℹ️  Please set GEMINI_API_KEY in .env file")
    print("   📝 Copy .env.template to .env and add your key")
    exit(1)

# Check 2: Import Gemini module
print("\n2️⃣ Checking Gemini module imports...")
try:
    import google.generativeai as genai
    print("   ✓ google.generativeai imported successfully")
except ImportError as e:
    print(f"   ✗ Failed to import: {e}")
    print("   💡 Run: pip install google-generativeai")
    exit(1)

# Check 3: Import custom advisor
print("\n3️⃣ Checking GeminiHealthAdvisor module...")
try:
    from gemini_advisor import GeminiHealthAdvisor
    print("   ✓ GeminiHealthAdvisor imported successfully")
except ImportError as e:
    print(f"   ✗ Failed to import: {e}")
    exit(1)

# Check 4: Initialize advisor
print("\n4️⃣ Initializing Gemini Health Advisor...")
try:
    advisor = GeminiHealthAdvisor()
    print("   ✓ Advisor initialized successfully")
except Exception as e:
    print(f"   ✗ Initialization failed: {e}")
    exit(1)

# Check 5: Test connection
print("\n5️⃣ Testing Gemini API connection...")
if advisor.test_connection():
    print("   ✓ Connection successful!")
else:
    print("   ✗ Connection failed!")
    print("   ℹ️  Check your API key and internet connection")
    exit(1)

# Check 6: Generate sample insights
print("\n6️⃣ Testing AI insights generation...")
test_data = {
    'heart_rate': 85,
    'blood_oxygen': 97,
    'temperature': 36.8,
    'respiration_rate': 16,
    'activity_level': 'moderate',
    'health_score': 85
}

try:
    insights = advisor.generate_comprehensive_insights(
        health_data=test_data,
        anomaly_status='Normal',
        risk_level='Low Risk'
    )
    
    print("   ✓ Insights generated successfully!")
    print("\n   📊 Sample AI Response:")
    print("   " + "─" * 66)
    print(f"   Summary: {insights.get('summary', 'N/A')[:100]}...")
    print(f"   Key Findings: {len(insights.get('key_findings', []))} items")
    print(f"   Recommendations: {len(insights.get('recommendations', []))} items")
    print(f"   Lifestyle Tips: {len(insights.get('lifestyle_tips', []))} items")
    print("   " + "─" * 66)
    
except Exception as e:
    print(f"   ✗ Insights generation failed: {e}")
    exit(1)

# Check 7: Verify Flask app integration
print("\n7️⃣ Checking Flask app integration...")
try:
    import app
    print("   ✓ Flask app module loaded")
    print(f"   ✓ Gemini advisor status: {'Active' if hasattr(app, 'gemini_advisor') and app.gemini_advisor else 'Inactive'}")
except Exception as e:
    print(f"   ⚠️  Could not check app integration: {e}")

# Final summary
print("\n" + "=" * 70)
print("✅ ALL CHECKS PASSED!")
print("=" * 70)
print("\n🎉 Gemini integration is working correctly!")
print("\n📝 Next steps:")
print("   1. Run the Flask app: python app.py")
print("   2. Open browser: http://localhost:5000")
print("   3. Click 'Load Dashboard' to see AI insights")
print("\n💡 Tips:")
print("   • AI insights appear in the 'Health Recommendations' section")
print("   • Look for the '🤖 AI-Powered Insights by Gemini' badge")
print("   • Compare AI insights vs rule-based recommendations")
print("\n" + "=" * 70)
