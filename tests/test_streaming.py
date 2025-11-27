"""
Test script for streaming functionality
"""
import sys
import os
# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.ai import GeminiHealthAdvisor

def test_streaming():
    """Test the streaming insights generation"""
    print("=" * 70)
    print("🧪 TESTING STREAMING FUNCTIONALITY")
    print("=" * 70)
    
    # Check if API key is available
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("\n⚠️  GEMINI_API_KEY not found in environment")
        print("   Streaming test cannot proceed without API key")
        return
    
    print(f"\n✓ API Key found: {api_key[:10]}...{api_key[-4:]}")
    
    # Initialize advisor
    try:
        advisor = GeminiHealthAdvisor()
        print("✓ GeminiHealthAdvisor initialized")
    except Exception as e:
        print(f"✗ Failed to initialize advisor: {e}")
        return
    
    # Test data
    health_data = {
        'heart_rate': 85,
        'blood_oxygen': 97,
        'temperature': 36.8,
        'respiration_rate': 16,
        'activity_level': 'moderate',
        'health_score': 85
    }
    
    print("\n🔄 Testing streaming insights generation...")
    print("-" * 70)
    
    try:
        full_response = ""
        chunk_count = 0
        
        for chunk in advisor.generate_comprehensive_insights_stream(
            health_data=health_data,
            anomaly_status='Normal',
            risk_level='Low Risk'
        ):
            chunk_count += 1
            full_response += chunk
            # Show first few characters of each chunk
            preview = chunk[:50].replace('\n', ' ')
            print(f"  Chunk {chunk_count}: {preview}...")
        
        print("-" * 70)
        print(f"\n✓ Streaming completed!")
        print(f"  Total chunks received: {chunk_count}")
        print(f"  Total length: {len(full_response)} characters")
        
        # Try to parse the response
        print("\n📊 Attempting to parse response...")
        import json
        try:
            # Clean up response
            cleaned = full_response.replace('```json\n', '').replace('```\n', '').replace('```', '').strip()
            insights = json.loads(cleaned)
            print("✓ Successfully parsed JSON response")
            print(f"  Keys: {list(insights.keys())}")
            if 'summary' in insights:
                print(f"\n  Summary: {insights['summary'][:100]}...")
        except json.JSONDecodeError as e:
            print(f"⚠️  JSON parsing failed: {e}")
            print(f"  Response preview: {full_response[:200]}...")
        
        print("\n" + "=" * 70)
        print("✅ STREAMING TEST COMPLETED SUCCESSFULLY")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n✗ Streaming test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    # Load environment
    from dotenv import load_dotenv
    load_dotenv()
    
    test_streaming()
