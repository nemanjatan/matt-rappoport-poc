import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

class AIConfig:
    # Providers
    PROVIDER_OPENAI = 'openai'
    PROVIDER_GEMINI = 'gemini'
    
    # Models
    MODEL_GPT4_VISION = 'gpt-4o' # or 'gpt-4-turbo'
    MODEL_GEMINI_PRO = 'gemini-1.5-pro'
    
    @staticmethod
    def get_api_key(provider: str) -> str:
        if provider == AIConfig.PROVIDER_OPENAI:
            return os.getenv('OPENAI_API_KEY')
        elif provider == AIConfig.PROVIDER_GEMINI:
            return os.getenv('GEMINI_API_KEY')
        return None
        
    @staticmethod
    def get_default_model(provider: str) -> str:
        if provider == AIConfig.PROVIDER_OPENAI:
            return AIConfig.MODEL_GPT4_VISION
        elif provider == AIConfig.PROVIDER_GEMINI:
            return AIConfig.MODEL_GEMINI_PRO
        return None
