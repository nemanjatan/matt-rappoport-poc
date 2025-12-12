import pytest
import os
from src.extractor import Extractor
from src.parser import Parser

IMG_PATH = "examples/IMG_1805.png"

@pytest.fixture(scope="module")
def real_ocr_data():
    if not os.path.exists(IMG_PATH):
        pytest.skip(f"Test image not found at {IMG_PATH}")
    extractor = Extractor(IMG_PATH)
    return extractor.extract()

def test_extract_product_info_integration(real_ocr_data):
    result = Parser.extract_product_info(real_ocr_data)
    print(f"\nExtracted Product Info: {result}")
    
    assert 'items' in result
    assert 'make_model' in result
    
    # Check if we caught the "Platine" line (Platinum)
    assert "Platine" in result['make_model'] or "Platinum" in result['make_model']
    
    # Check if we captured "BOD ners" (OCR for Appliances)
    assert "BOD" in result['items'] or "Appliances" in result['items']
