from src.extractor import Extractor
from src.parser import Parser
from datetime import datetime
import os
from src.logger import setup_logger

logger = setup_logger()

def extract_all_data(image_path: str) -> dict:
    """
    Main orchestration function to extract all data from a finance agreement image.
    """
    logger.info(f"Starting pipeline for {image_path}")
    
    # 1. OCR Extraction
    try:
        extractor = Extractor(image_path)
        ocr_data = extractor.extract()
    except Exception as e:
        logger.critical(f"Pipeline stopped due to OCR failure: {e}")
        raise
    
    # 2. Parsing Steps
    logger.info("Starting parsing steps")
    seller_info = Parser.extract_seller_info(ocr_data)
    buyer_info = Parser.extract_buyer_info(ocr_data)
    product_info = Parser.extract_product_info(ocr_data)
    financial_data = Parser.extract_financial_data(ocr_data)
    payment_details = Parser.extract_payment_details(ocr_data)
    itemization = Parser.extract_itemization(ocr_data)
    
    # 3. Assemble Result
    result = {
        'seller': seller_info,
        'buyer': buyer_info,
        'product': product_info,
        'financial': financial_data,
        'payment': payment_details,
        'itemization': itemization,
        'metadata': {
            'source_file': os.path.basename(image_path),
            'extraction_date': datetime.now().isoformat(),
            'ocr_engine': 'Tesseract',
            'poc_version': '1.0'
        }
    }
    
    logger.info("Pipeline completed successfully")
    return result
