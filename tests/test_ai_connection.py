import pytest
import os
from src.ai_config import AIConfig
from src.ai_extractor import AIVisionExtractor

@pytest.mark.skipif(not os.getenv('OPENAI_API_KEY'), reason="No OpenAI API Key")
def test_openai_connection():
    extractor = AIVisionExtractor(provider=AIConfig.PROVIDER_OPENAI)
    assert extractor.client is not None
    # We won't make a real call to save cost/time, just check init

@pytest.mark.skipif(not os.getenv('GEMINI_API_KEY'), reason="No Gemini API Key")
def test_gemini_connection():
    extractor = AIVisionExtractor(provider=AIConfig.PROVIDER_GEMINI)
    assert extractor.client is not None

def test_config_defaults():
    # Test that defaults work (even if keys slightly missing, logic holds)
    assert AIConfig.get_default_model('openai') == 'gpt-4o'
    assert AIConfig.get_default_model('gemini') == 'gemini-1.5-pro'
