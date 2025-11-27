"""
AI module for Health Monitoring System
Contains Gemini AI integration
"""

try:
    from .gemini_advisor import GeminiHealthAdvisor
    __all__ = ['GeminiHealthAdvisor']
except ImportError:
    __all__ = []
