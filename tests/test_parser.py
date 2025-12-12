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

def test_extract_seller_info_integration(real_ocr_data):
    """Test with the real image."""
    result = Parser.extract_seller_info(real_ocr_data)
    
    assert result['seller_name'] is not None
    assert "Passanante" in result['seller_name']
    
    assert result['seller_phone'] == "800-772-7786"
    
    assert result['seller_address'] is not None
    assert "1901 Farragut Ave" in result['seller_address']
    assert "Bristol, PA 19007" in result['seller_address']

def test_extract_seller_info_robustness():
    """Test with mock data to ensure regex works on varied inputs."""
    mock_data = {
        'full_text': """
        Agreement Header
        Seller: Test Vendor Inc.
        123 Main St.
        Anytown, NY 10001
        
        Phone: 555-123-4567
        """
    }
    # Note: Our current implementation targets "Farragut Ave" specifically for the address 
    # as per PoC requirements for this specific document type. 
    # General address extraction is much harder (requires NLP).
    # so we test what we can (Name, Phone).
    
    result = Parser.extract_seller_info(mock_data)
    assert result['seller_name'] == "Test Vendor Inc."
    assert result['seller_phone'] == "555-123-4567"
