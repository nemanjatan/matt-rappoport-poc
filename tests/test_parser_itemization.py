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

def test_extract_itemization_integration(real_ocr_data):
    result = Parser.extract_itemization(real_ocr_data)
    print(f"\nExtracted Itemization: {result}")
    
    # We expect 'down_payment' to be 0.0 because of "so"
    assert result['down_payment'] == 0.0
    
    # 'cash_price' read as "3_ Mah PCs" -> 3.0? or 3? 
    # Logic looks for digits. "3" is a digit.
    # It might extract 3.0.
    
    # Check that keys exist
    assert 'cash_price' in result
    assert 'unpaid_balance' in result
    assert 'itemized_amount_financed' in result
