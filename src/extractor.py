import pytesseract
from pytesseract import Output
from src.preprocessor import preprocess_image
from src.logger import setup_logger
import pandas as pd

logger = setup_logger()

class Extractor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        logger.debug(f"Extractor initialized for {file_path}")

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
        try:
            image = preprocess_image(self.file_path)
            logger.debug("Image preprocessing complete")
        except Exception as e:
            logger.error(f"Preprocessing failed: {e}")
            raise

        # 2. Get Full Text (Backup/Simple View)
        try:
            full_text = pytesseract.image_to_string(image)
            logger.debug("Full text extraction complete")
        except Exception as e:
            logger.error(f"OCR Full Text failed: {e}")
            raise

        # 3. Get Detailed Data (Words + Boxes)
        # image_to_data returns a TSV-like string or dict. Output.DICT is easiest.
        try:
            data = pytesseract.image_to_data(image, output_type=Output.DICT)
            logger.debug("Ocr word data extraction complete")
        except Exception as e:
            logger.error(f"OCR Data failed: {e}")
            raise

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
            
        logger.info(f"Extraction complete. Found {len(word_data)} words.")

        return {
            'full_text': full_text,
            'word_data': word_data
        }

    def extract(self):
        # Alias for backward compatibility or main entry point
        return self.extract_text_with_layout()
