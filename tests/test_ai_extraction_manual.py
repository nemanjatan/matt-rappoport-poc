import os
import sys
import json

# Ensure src can be found
sys.path.append(os.getcwd())

from src.ai_extractor import AIVisionExtractor

def test_ai_manual(image_path):
    print(f"Testing AI Extraction on {image_path}...")
    
    # Try OpenAI first, fallback to Gemini or just error
    try:
        extractor = AIVisionExtractor(provider='openai') # or 'gemini'
    except Exception as e:
        print(f"Setup failed: {e}")
        return

    fields = ['seller', 'buyer', 'financial', 'payment', 'product']
    
    for field in fields:
        print(f"\n--- Extracting {field.upper()} ---")
        try:
            data = extractor.extract_field(image_path, field)
            print(json.dumps(data, indent=2))
        except Exception as e:
            print(f"Failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 tests/test_ai_extraction_manual.py <image_path>")
        sys.exit(1)
        
    test_ai_manual(sys.argv[1])
