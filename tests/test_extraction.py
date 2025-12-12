import pytest
import os
from src.extractor import Extractor

IMG_PATH = "examples/IMG_1805.png"

def test_extractor_initialization():
    extractor = Extractor(IMG_PATH)
    assert extractor.file_path == IMG_PATH

def test_extract_text_with_layout_returns_structure():
    """Verifies that the extractor returns the expected dictionary structure."""
    if not os.path.exists(IMG_PATH):
        pytest.skip(f"Test image not found at {IMG_PATH}")
        
    extractor = Extractor(IMG_PATH)
    result = extractor.extract_text_with_layout()
    
    assert 'full_text' in result
    assert 'word_data' in result
    assert isinstance(result['full_text'], str)
    assert isinstance(result['word_data'], list)
    
    # Check for content if list is not empty (it shouldn't be for this image)
    if result['word_data']:
        first_word = result['word_data'][0]
        assert 'text' in first_word
        assert 'left' in first_word
        assert 'conf' in first_word

def test_extract_contains_critical_keywords():
    """Checks if OCR reasonably captured the title or key terms."""
    if not os.path.exists(IMG_PATH):
        pytest.skip(f"Test image not found at {IMG_PATH}")
        
    extractor = Extractor(IMG_PATH)
    result = extractor.extract()
    full_text = result['full_text'].upper()
    
    # Check for known keywords likely to appear
    # Note: OCR might make mistakes, so we check for substrings
    keywords = ["AGREEMENT", "PASSANANTE", "CREDIT"] 
    found = [k for k in keywords if k in full_text]
    
    # Use a soft assertion - at least one keyword should be found
    assert len(found) > 0, f"OCR failed to find any expected keywords. Found text sample: {full_text[:100]}"
