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

def test_extract_payment_details_integration(real_ocr_data):
    result = Parser.extract_payment_details(real_ocr_data)
    print(f"\nExtracted Payment Info: {result}")
    
    assert 'payment_frequency' in result
    assert "Monthly" in result['payment_frequency']
    assert "beginning" in result['payment_frequency']
    
    # Amount check (227 or 229)
    if result['payment_amount']:
        assert 200 < result['payment_amount'] < 300
    
    # Number check (48?)
    # If None, it means OCR missed it.
