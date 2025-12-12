import pytesseract
from pytesseract import Output
from src.preprocessor import preprocess_image
import pandas as pd

class Extractor:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract_text_with_layout(self) -> dict:
        """
        Extracts text from the image using OCR, returning full text and detailed layout data.
        
        Returns:
            dict: {
                'full_text': str,
                'word_data': list[dict] # {'text', 'conf', 'left', 'top', 'width', 'height'}
            }
        """
        # 1. Preprocess
        # We don't save the debug image here by default, pass output_path if needed
        image = preprocess_image(self.file_path)

        # 2. Get Full Text (Backup/Simple View)
        full_text = pytesseract.image_to_string(image)

        # 3. Get Detailed Data (Words + Boxes)
        # image_to_data returns a TSV-like string or dict. Output.DICT is easiest.
        data = pytesseract.image_to_data(image, output_type=Output.DICT)

        # 4. Process into a cleaner list of dicts
        word_data = []
        n_boxes = len(data['level'])
        
        for i in range(n_boxes):
            text = data['text'][i].strip()
            if not text:
                continue
                
            word_data.append({
                'text': text,
                'left': data['left'][i],
                'top': data['top'][i],
                'width': data['width'][i],
                'height': data['height'][i],
                'conf': int(data['conf'][i]) # Confidence 0-100
            })

        return {
            'full_text': full_text,
            'word_data': word_data
        }

    def extract(self):
        # Alias for backward compatibility or main entry point
        return self.extract_text_with_layout()
