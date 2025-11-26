"""
Gemini AI Integration for Health Insights
Provides AI-powered health recommendations using Google's Gemini API
"""

import google.generativeai as genai
import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeminiHealthAdvisor:
    """Uses Gemini AI to generate personalized health insights and recommendations"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini Health Advisor
        
        Parameters:
        - api_key: Gemini API key (if None, will try to get from environment)
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Please set GEMINI_API_KEY environment variable "
                "or pass it directly to the constructor."
            )
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # System context for health advisory
        self.system_context = """You are an expert AI health advisor with deep knowledge in:
- General health and wellness
- Vital signs interpretation
- Preventive healthcare
- Lifestyle recommendations
- When to seek medical attention

Your role is to:
1. Analyze health metrics and patterns
2. Provide clear, actionable recommendations
3. Flag concerning trends that need medical attention
4. Offer lifestyle and wellness advice
5. Be empathetic and encouraging

Important guidelines:
- Always prioritize safety and recommend professional medical care when needed
- Use simple, clear language that anyone can understand
- Be specific with recommendations
- Use emojis sparingly but effectively
- Keep recommendations concise but comprehensive
- Never diagnose specific diseases or conditions
- Always remind users you're an AI assistant, not a replacement for doctors
"""
        
        logger.info("✓ Gemini Health Advisor initialized successfully")
    
    def generate_comprehensive_insights(
        self, 
        health_data: Dict, 
        anomaly_status: str, 
        risk_level: str,
        historical_trends: Optional[Dict] = None
    ) -> Dict:
        """
        Generate comprehensive AI-powered health insights
        
        Parameters:
        - health_data: Current health metrics
        - anomaly_status: 'Normal' or 'Anomaly'
        - risk_level: 'Low Risk', 'Medium Risk', or 'High Risk'
        - historical_trends: Optional historical data for trend analysis
        
        Returns:
        - Dictionary with recommendations, insights, and analysis
        """
        try:
            # Prepare the prompt
            prompt = self._create_health_analysis_prompt(
                health_data, anomaly_status, risk_level, historical_trends
            )
            
            # Generate insights
            logger.info("🤖 Requesting insights from Gemini AI...")
            response = self.model.generate_content(prompt)
            
            # Parse the response
            insights = self._parse_gemini_response(response.text)
            
            logger.info("✓ Gemini AI insights generated successfully")
            return insights
            
        except Exception as e:
            logger.error(f"Error generating Gemini insights: {str(e)}")
            # Fallback to rule-based recommendations
            return self._fallback_recommendations(health_data, anomaly_status, risk_level)
    
    def _create_health_analysis_prompt(
        self, 
        health_data: Dict, 
        anomaly_status: str, 
        risk_level: str,
        historical_trends: Optional[Dict]
    ) -> str:
        """Create a detailed prompt for Gemini AI"""
        
        prompt = f"""{self.system_context}

## Current Health Assessment

**User's Current Vital Signs:**
- Heart Rate: {health_data.get('heart_rate', 'N/A')} bpm
- Blood Oxygen (SpO2): {health_data.get('blood_oxygen', 'N/A')}%
- Body Temperature: {health_data.get('temperature', 'N/A')}°C
- Respiration Rate: {health_data.get('respiration_rate', 'N/A')} breaths/min
- Activity Level: {health_data.get('activity_level', 'N/A')}
- Recent Steps: {health_data.get('steps', 'N/A')}

**AI Analysis Results:**
- Anomaly Detection: {anomaly_status}
- Risk Assessment: {risk_level}
- Health Score: {health_data.get('health_score', 'N/A')}/100

**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        
        # Add historical trends if available
        if historical_trends:
            prompt += f"""
**Recent Trends (Last 20 readings):**
- Heart Rate Trend: {self._describe_trend(historical_trends.get('heart_rate', []))}
- Blood Oxygen Trend: {self._describe_trend(historical_trends.get('blood_oxygen', []))}
- Temperature Trend: {self._describe_trend(historical_trends.get('temperature', []))}

"""
        
        prompt += """
## Your Task

Please provide a comprehensive health analysis in the following JSON format:

{
  "summary": "Brief 1-2 sentence overview of the person's current health status",
  "key_findings": [
    "Finding 1 about their vitals",
    "Finding 2 about patterns or concerns",
    "Finding 3 about positive aspects"
  ],
  "recommendations": [
    "Specific actionable recommendation 1",
    "Specific actionable recommendation 2",
    "Specific actionable recommendation 3",
    "Additional recommendations as needed"
  ],
  "immediate_actions": [
    "Any urgent actions needed (empty array if none)"
  ],
  "lifestyle_tips": [
    "Lifestyle tip 1",
    "Lifestyle tip 2",
    "Lifestyle tip 3"
  ],
  "monitoring_advice": "What should the user monitor or watch for",
  "when_to_seek_help": "Clear guidance on when to contact a healthcare provider",
  "encouragement": "Positive, encouraging message"
}

**Important:** Return ONLY valid JSON. Do not include markdown formatting, code blocks, or any text outside the JSON structure.
"""
        
        return prompt
    
    def _describe_trend(self, values: List) -> str:
        """Describe a trend in simple terms"""
        if not values or len(values) < 2:
            return "insufficient data"
        
        start_avg = sum(values[:5]) / min(5, len(values))
        end_avg = sum(values[-5:]) / min(5, len(values[-5:]))
        
        diff = end_avg - start_avg
        
        if abs(diff) < 1:
            return "stable"
        elif diff > 0:
            return f"increasing (up by {diff:.1f})"
        else:
            return f"decreasing (down by {abs(diff):.1f})"
    
    def _parse_gemini_response(self, response_text: str) -> Dict:
        """Parse Gemini's JSON response"""
        try:
            # Clean the response - remove markdown code blocks if present
            cleaned = response_text.strip()
            if cleaned.startswith('```json'):
                cleaned = cleaned[7:]
            if cleaned.startswith('```'):
                cleaned = cleaned[3:]
            if cleaned.endswith('```'):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()
            
            # Parse JSON
            insights = json.loads(cleaned)
            
            # Validate structure
            required_keys = ['summary', 'key_findings', 'recommendations']
            if not all(key in insights for key in required_keys):
                raise ValueError("Missing required keys in Gemini response")
            
            return insights
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini JSON response: {str(e)}")
            logger.error(f"Raw response: {response_text[:500]}")
            raise
    
    # def _fallback_recommendations(
    #     self, 
    #     health_data: Dict, 
    #     anomaly_status: str, 
    #     risk_level: str
    # ) -> Dict:
    #     """Fallback to rule-based recommendations if Gemini fails"""
    #     logger.warning("⚠️ Using fallback rule-based recommendations")
        
    #     recommendations = []
    #     immediate_actions = []
    #     key_findings = []
        
    #     # Heart rate analysis
    #     hr = health_data.get('heart_rate', 75)
    #     if hr < 60:
    #         key_findings.append(f"Heart rate is low at {hr} bpm (normal: 60-100)")
    #         recommendations.append("Consider consulting a healthcare provider about your low heart rate")
    #     elif hr > 100:
    #         key_findings.append(f"Heart rate is elevated at {hr} bpm (normal: 60-100)")
    #         recommendations.append("Try relaxation techniques like deep breathing")
    #         recommendations.append("Reduce caffeine intake and ensure adequate hydration")
    #     else:
    #         key_findings.append(f"Heart rate is normal at {hr} bpm")
        
    #     # Blood oxygen analysis
    #     spo2 = health_data.get('blood_oxygen', 98)
    #     if spo2 < 90:
    #         key_findings.append(f"Blood oxygen is critically low at {spo2}%")
    #         immediate_actions.append("URGENT: Seek immediate medical attention - oxygen levels critically low!")
    #     elif spo2 < 95:
    #         key_findings.append(f"Blood oxygen is below normal at {spo2}%")
    #         recommendations.append("Ensure good ventilation and avoid strenuous activities")
    #     else:
    #         key_findings.append(f"Blood oxygen is good at {spo2}%")
        
    #     # Temperature analysis
    #     temp = health_data.get('temperature', 36.6)
    #     if temp > 38.0:
    #         key_findings.append(f"Fever detected at {temp}°C")
    #         immediate_actions.append("Consider taking fever-reducing medication and consult a doctor")
    #     elif temp > 37.5:
    #         key_findings.append(f"Temperature slightly elevated at {temp}°C")
    #         recommendations.append("Stay hydrated and monitor your temperature")
    #     elif temp < 36.0:
    #         key_findings.append(f"Body temperature is low at {temp}°C")
    #         recommendations.append("Warm up and monitor for hypothermia symptoms")
    #     else:
    #         key_findings.append(f"Temperature is normal at {temp}°C")
        
    #     # Risk-based recommendations
    #     if risk_level == 'High Risk':
    #         immediate_actions.append("Schedule an immediate consultation with your healthcare provider")
    #     elif risk_level == 'Medium Risk':
    #         recommendations.append("Schedule a check-up with your healthcare provider within 24-48 hours")
        
    #     # General recommendations
    #     recommendations.extend([
    #         "Maintain a balanced diet rich in fruits and vegetables",
    #         "Aim for 7-9 hours of quality sleep each night",
    #         "Stay physically active - aim for 30 minutes of exercise daily",
    #         "Stay hydrated - drink 8 glasses of water daily"
    #     ])
        
    #     return {
    #         "summary": f"Your vital signs show {anomaly_status.lower()} patterns with {risk_level.lower()}.",
    #         "key_findings": key_findings[:3],
    #         "recommendations": recommendations[:5],
    #         "immediate_actions": immediate_actions,
    #         "lifestyle_tips": [
    #             "Regular exercise improves cardiovascular health",
    #             "Stress management through meditation or yoga",
    #             "Maintain a consistent sleep schedule"
    #         ],
    #         "monitoring_advice": "Continue monitoring your vitals regularly and track any changes",
    #         "when_to_seek_help": "Contact a healthcare provider if symptoms worsen or if you experience chest pain, severe shortness of breath, or persistent fever",
    #         "encouragement": "Keep up the good work monitoring your health! Regular tracking helps catch issues early."
    #     }
    
    def generate_quick_insight(self, health_data: Dict) -> str:
        """Generate a quick single-line insight"""
        try:
            prompt = f"""As a health advisor, provide ONE brief sentence (max 15 words) about these vitals:
Heart Rate: {health_data.get('heart_rate')} bpm, 
Blood Oxygen: {health_data.get('blood_oxygen')}%, 
Temperature: {health_data.get('temperature')}°C

Just the sentence, nothing else."""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except:
            return "Your vitals are being monitored. Stay healthy!"
    
    def test_connection(self) -> bool:
        """Test if Gemini API is accessible"""
        try:
            response = self.model.generate_content("Say 'connected' if you can read this.")
            return 'connect' in response.text.lower()
        except Exception as e:
            logger.error(f"Gemini connection test failed: {str(e)}")
            return False


# Usage example
if __name__ == "__main__":
    print("="*70)
    print("🤖 Gemini Health Advisor - Test")
    print("="*70)
    
    # Check for API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("\n⚠️  GEMINI_API_KEY not found in environment variables")
        print("Please set it with: export GEMINI_API_KEY='your-api-key'")
        print("Or create a .env file with: GEMINI_API_KEY=your-api-key")
        exit(1)
    
    try:
        # Initialize advisor
        advisor = GeminiHealthAdvisor()
        
        # Test connection
        print("\n📡 Testing Gemini API connection...")
        if advisor.test_connection():
            print("✓ Connected to Gemini AI successfully!")
        else:
            print("✗ Connection test failed")
            exit(1)
        
        # Test health data
        sample_health_data = {
            'heart_rate': 145,
            'blood_oxygen': 94,
            'temperature': 37.8,
            'respiration_rate': 22,
            'activity_level': 'high',
            'steps': 8500,
            'health_score': 72
        }
        
        print("\n🏥 Generating AI-powered health insights...")
        print(f"Sample data: HR={sample_health_data['heart_rate']}, "
              f"SpO2={sample_health_data['blood_oxygen']}%, "
              f"Temp={sample_health_data['temperature']}°C")
        
        # Generate insights
        insights = advisor.generate_comprehensive_insights(
            health_data=sample_health_data,
            anomaly_status='Anomaly',
            risk_level='Medium Risk'
        )
        
        # Display results
        print("\n" + "="*70)
        print("📊 AI-GENERATED HEALTH INSIGHTS")
        print("="*70)
        
        print(f"\n📝 Summary:\n{insights['summary']}")
        
        print("\n🔍 Key Findings:")
        for i, finding in enumerate(insights['key_findings'], 1):
            print(f"  {i}. {finding}")
        
        print("\n💡 Recommendations:")
        for i, rec in enumerate(insights['recommendations'], 1):
            print(f"  {i}. {rec}")
        
        if insights.get('immediate_actions'):
            print("\n⚠️  IMMEDIATE ACTIONS NEEDED:")
            for action in insights['immediate_actions']:
                print(f"  • {action}")
        
        print("\n🌟 Lifestyle Tips:")
        for tip in insights.get('lifestyle_tips', []):
            print(f"  • {tip}")
        
        print(f"\n👀 Monitoring Advice:\n{insights.get('monitoring_advice', 'N/A')}")
        print(f"\n🏥 When to Seek Help:\n{insights.get('when_to_seek_help', 'N/A')}")
        print(f"\n💪 Encouragement:\n{insights.get('encouragement', 'Keep monitoring!')}")
        
        print("\n" + "="*70)
        print("✅ Test completed successfully!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
