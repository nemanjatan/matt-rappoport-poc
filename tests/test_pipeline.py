import pytest
import os
from src.pipeline import extract_all_data

IMG_PATH = "examples/IMG_1805.png"

def test_extract_all_data_structure():
    if not os.path.exists(IMG_PATH):
        pytest.skip("Image not found")
        
    result = extract_all_data(IMG_PATH)
    
    # Verify Top Level Keys
    assert 'seller' in result
    assert 'buyer' in result
    assert 'product' in result
    assert 'financial' in result
    assert 'payment' in result
    assert 'itemization' in result
    assert 'metadata' in result
    
    # Verify Content (Spot Checks)
    assert "Passanante" in result['seller']['seller_name']
    assert 227.0 == result['payment']['payment_amount']
    assert 3667.22 == result['financial']['finance_charge']
    
    # Metadata
    assert result['metadata']['source_file'] == "IMG_1805.png"
    assert result['metadata']['ocr_engine'] == "Tesseract"
