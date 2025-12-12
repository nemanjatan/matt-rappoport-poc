import pytest
import os
from PIL import Image
from src.preprocessor import preprocess_image

IMG_PATH = "examples/IMG_1805.png"
OUTPUT_PATH = "examples/IMG_1805_processed.png"

def test_preprocess_image_executes():
    """Takes the example image, processes it, and verifies output is an image."""
    if not os.path.exists(IMG_PATH):
        pytest.skip(f"Test image not found at {IMG_PATH}")
    
    # Run processing
    processed_img = preprocess_image(IMG_PATH, output_path=OUTPUT_PATH)
    
    # Assert return type
    assert isinstance(processed_img, Image.Image)
    
    # Assert output file created
    assert os.path.exists(OUTPUT_PATH)
    
    # Verify it is grayscale (mode 'L') or bilevel ('1') usually, but fromarray makes it 'L' or 'RGB' depending on input. 
    # Our opencv binary image is single channel -> 'L'.
    assert processed_img.mode == 'L'

def test_preprocess_raises_on_missing_file():
    with pytest.raises(FileNotFoundError):
        preprocess_image("non_existent.png")
