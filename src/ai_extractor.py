import base64
import os
import json
import re
from src.ai_config import AIConfig
from src.logger import setup_logger

# Import providers
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

logger = setup_logger()

class AIVisionExtractor:
    PROMPTS = {
        "seller": "Extract the seller information from this finance agreement. Look for the seller name, address, and phone number in the header section. Return as valid JSON: {\"seller_name\": str, \"seller_address\": str, \"seller_phone\": str}. If not found, use null.",
        "buyer": "Extract buyer and co-buyer information. Find buyer name, address, phone, and co-buyer name, address, phone. Note: This section might be handwritten. Return as valid JSON: {\"buyer_name\": str, \"buyer_address\": str, \"buyer_phone\": str, \"co_buyer_name\": str, \"co_buyer_address\": str, \"co_buyer_phone\": str}. If not found, use null.",
        "financial": "Extract financial data from the Truth in Lending section. Find APR percentage, finance charge, amount financed, total of payments, total sales price. Return numeric values only (no currency symbols). Return as valid JSON: {\"apr_percentage\": float, \"finance_charge\": float, \"amount_financed\": float, \"total_of_payments\": float, \"total_sales_price\": float}. If not found, use null.",
        "payment": "Extract payment schedule: number of payments, payment amount, payment frequency. Return as valid JSON: {\"number_of_payments\": int, \"payment_amount\": float, \"payment_frequency\": str}. If not found, use null.",
        "product": "Extract product details: quantity, items description, make/model. Return as valid JSON: {\"quantity\": str, \"items\": str, \"make_model\": str}. If not found, use null.",
        "itemization": "Extract itemization: cash price, down payment, unpaid balance, amounts paid to others, amount financed. Return numeric values. Return as valid JSON: {\"cash_price\": float, \"down_payment\": float, \"unpaid_balance\": float, \"amounts_paid_to_others\": float, \"itemized_amount_financed\": float}. If not found, use null."
    }

    def __init__(self, provider: str = AIConfig.PROVIDER_OPENAI, model: str = None):
        self.provider = provider
        self.model = model or AIConfig.get_default_model(provider)
        self.api_key = AIConfig.get_api_key(provider)
        
        if not self.api_key:
            logger.warning(f"No API key found for provider {provider}. AI features will fail.")
            
        self.client = None
        self._setup_client()

    def _setup_client(self):
        if self.provider == AIConfig.PROVIDER_OPENAI:
            if OpenAI:
                self.client = OpenAI(api_key=self.api_key)
            else:
                logger.error("OpenAI package not installed.")
        elif self.provider == AIConfig.PROVIDER_GEMINI:
            if genai:
                genai.configure(api_key=self.api_key)
                self.client = genai.GenerativeModel(self.model)
            else:
                logger.error("Google Generative AI package not installed.")

    def _encode_image(self, image_path: str) -> str:
        """Encodes image to base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def extract_structured_data(self, image_path: str, prompt_text: str) -> str:
        """
        Sends image to AI provider and gets response text.
        Returns raw string (caller should parse JSON).
        """
        if not self.api_key:
            raise ValueError(f"API Key missing for {self.provider}")
            
        logger.info(f"Sending image to AI ({self.provider}/{self.model})...")
        
        try:
            if self.provider == AIConfig.PROVIDER_OPENAI:
                base64_image = self._encode_image(image_path)
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt_text},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    },
                                },
                            ],
                        }
                    ],
                    max_tokens=1000,
                )
                return response.choices[0].message.content

            elif self.provider == AIConfig.PROVIDER_GEMINI:
                # Gemini handles files differently, but for base64/bytes:
                # We can also upload file or pass data.
                # For simplicity in this PoC, let's use the PIL image if possible or path.
                import PIL.Image
                img = PIL.Image.open(image_path)
                response = self.client.generate_content([prompt_text, img])
                return response.text
                
        except Exception as e:
            logger.error(f"AI Extraction failed: {e}")
            raise

        return ""

    def parse_json_response(self, text: str) -> dict:
        """Parses JSON from API response, handling markdown blocks."""
        try:
            # 1. Remove markdown code blocks if present
            cleaned_text = re.sub(r"```json\s*", "", text)
            cleaned_text = re.sub(r"```", "", cleaned_text)
            cleaned_text = cleaned_text.strip()
            
            # 2. Parse JSON
            return json.loads(cleaned_text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from AI response: {e}. Raw Text: {text}")
            return {}

    def extract_field(self, image_path: str, field_type: str) -> dict:
        """
        Extracts a specific field category using the predefined prompt.
        """
        if field_type not in self.PROMPTS:
            raise ValueError(f"Unknown field type: {field_type}")
            
        prompt = self.PROMPTS[field_type]
        raw_response = self.extract_structured_data(image_path, prompt)
        
        return self.parse_json_response(raw_response)
