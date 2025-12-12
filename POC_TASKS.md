# Proof of Concept - Task Tickets

## Project Overview
Build a PoC tool to extract structured data from scanned finance agreement documents. This PoC focuses exclusively on processing `examples/IMG_1805.png` (a scanned "INSTALLMENT CREDIT AGREEMENT" document from Passanante's Home Food Service).

## Expected Output
The tool should extract all relevant data fields and export them to a structured format (CSV/Excel) ready for manual entry into loan software.

---

## Task 1: Project Setup and Dependencies
**Priority:** High  
**Status:** Pending

### Description
Set up the Python project structure with all necessary dependencies for OCR, image processing, and data export.

### Requirements
- Create a Python project with virtual environment support
- Install and configure dependencies:
  - OCR library (e.g., `pytesseract` with Tesseract OCR engine, or `easyocr`, or `paddleocr`)
  - Image processing library (`Pillow`/`PIL`)
  - Data export library (`pandas`, `openpyxl` for Excel support)
  - Optional: `pdf2image` if converting PDFs later
- Create a `requirements.txt` file
- Create a `README.md` with setup instructions
- Set up project structure:
  ```
  /
  ├── src/
  │   ├── __init__.py
  │   ├── extractor.py
  │   ├── validator.py
  │   └── exporter.py
  ├── tests/
  │   ├── __init__.py
  │   └── test_extraction.py
  ├── examples/
  │   └── IMG_1805.png
  ├── requirements.txt
  └── README.md
  ```

### Acceptance Criteria
- [ ] Project can be set up with `pip install -r requirements.txt`
- [ ] All dependencies are properly documented
- [ ] Project structure follows best practices

---

## Task 2: Image Preprocessing Module
**Priority:** High  
**Status:** Pending

### Description
Create a module to preprocess the scanned image (`examples/IMG_1805.png`) to improve OCR accuracy.

### Requirements
- Load and preprocess the image:
  - Convert to grayscale if needed
  - Apply noise reduction
  - Enhance contrast and sharpness
  - Deskew/rotate if necessary
  - Resize if needed for optimal OCR performance
- Create a function `preprocess_image(image_path: str) -> PIL.Image`
- Save preprocessed image for debugging/verification

### Acceptance Criteria
- [ ] Function successfully loads `examples/IMG_1805.png`
- [ ] Preprocessed image is clearer than original for OCR
- [ ] Preprocessing is configurable (can be adjusted if needed)

---

## Task 3: OCR Text Extraction Module
**Priority:** High  
**Status:** Pending

### Description
Extract all text from the preprocessed image using OCR, preserving layout information where possible.

### Requirements
- Implement OCR extraction using chosen library
- Extract text with bounding box coordinates (for layout-aware parsing)
- Handle both printed and handwritten text
- Create a function `extract_text_with_layout(image_path: str) -> dict` that returns:
  - Full text string
  - Text with coordinates (list of dicts: `{'text': str, 'x': int, 'y': int, 'width': int, 'height': int}`)
- Log OCR confidence scores for debugging

### Acceptance Criteria
- [ ] Successfully extracts text from `examples/IMG_1805.png`
- [ ] Handwritten fields (buyer name, addresses, phone numbers, amounts) are captured
- [ ] Printed text (labels, terms) are captured accurately
- [ ] Layout/position information is preserved

---

## Task 4: Data Extraction Module - Seller Information
**Priority:** Medium  
**Status:** Pending

### Description
Extract seller information from the document header.

### Requirements
- Extract from `examples/IMG_1805.png`:
  - Seller name: "Passanante's Home Food Service"
  - Seller address: "1901 Farragut Ave. Bristol, PA 19007"
  - Seller phone: "800-772-7786"
- Create function `extract_seller_info(ocr_data: dict) -> dict`
- Return structured dictionary:
  ```python
  {
    'seller_name': str,
    'seller_address': str,
    'seller_phone': str
  }
  ```

### Acceptance Criteria
- [ ] All seller fields extracted correctly from sample image
- [ ] Function handles missing fields gracefully (returns None/empty string)
- [ ] Extracted data matches expected values from IMG_1805.png

---

## Task 5: Data Extraction Module - Buyer Information
**Priority:** High  
**Status:** Pending

### Description
Extract buyer and co-buyer information from the document.

### Requirements
- Extract from `examples/IMG_1805.png`:
  - Buyer name: "Hannah Hornberse"
  - Buyer address: "500 Ricky Rd Mecheraustury PA 1255"
  - Buyer phone: "717-257-0626"
  - Co-buyer name: "Rany Hernberse"
  - Co-buyer address: "500 Ricky Rd Mecheraustury PA 1255" (same as buyer)
  - Co-buyer phone: "717-603-2240"
- Create function `extract_buyer_info(ocr_data: dict) -> dict`
- Return structured dictionary:
  ```python
  {
    'buyer_name': str,
    'buyer_address': str,
    'buyer_phone': str,
    'co_buyer_name': str,
    'co_buyer_address': str,
    'co_buyer_phone': str
  }
  ```

### Acceptance Criteria
- [ ] All buyer and co-buyer fields extracted correctly from sample image
- [ ] Handles handwritten text accurately
- [ ] Function handles missing fields gracefully

---

## Task 6: Data Extraction Module - Product Information
**Priority:** High  
**Status:** Pending

### Description
Extract product/service details from the "Goods or Services" section.

### Requirements
- Extract from `examples/IMG_1805.png`:
  - Quantity: "2"
  - Items: "Appliances"
  - Make/Model: "Platinum Couture / Cutler"
- Create function `extract_product_info(ocr_data: dict) -> dict`
- Return structured dictionary:
  ```python
  {
    'quantity': int,
    'items': str,
    'make_model': str
  }
  ```

### Acceptance Criteria
- [ ] All product fields extracted correctly from sample image
- [ ] Quantity is converted to integer
- [ ] Make/model handles special characters (forward slash)

---

## Task 7: Data Extraction Module - Financial Data (Truth in Lending)
**Priority:** High  
**Status:** Pending

### Description
Extract financial data from the "Truth in Lending Disclosures" section.

### Requirements
- Extract from `examples/IMG_1805.png`:
  - Annual Percentage Rate (APR): "21" (as percentage, e.g., 21.0)
  - Finance Charge: "$3607.72" (as float, e.g., 3607.72)
  - Amount Financed: "$6998" (as float, e.g., 6998.0)
  - Total of Payments: "$11,025.76" (as float, e.g., 11025.76)
  - Total Sales Price: "$11,025.76" (as float, e.g., 11025.76)
- Create function `extract_financial_data(ocr_data: dict) -> dict`
- Return structured dictionary:
  ```python
  {
    'apr_percentage': float,
    'finance_charge': float,
    'amount_financed': float,
    'total_of_payments': float,
    'total_sales_price': float
  }
  ```
- Clean currency symbols and commas from extracted values
- Convert to appropriate numeric types

### Acceptance Criteria
- [ ] All financial fields extracted correctly from sample image
- [ ] Currency symbols and formatting are properly removed
- [ ] Values are converted to correct numeric types (float)
- [ ] Handles handwritten dollar amounts accurately

---

## Task 8: Data Extraction Module - Payment Details
**Priority:** High  
**Status:** Pending

### Description
Extract payment schedule information.

### Requirements
- Extract from `examples/IMG_1805.png`:
  - Number of Payments: "48"
  - Amount of Payments: "$229.70" (as float, e.g., 229.70)
  - When Payments Are Due: "Monthly, beginning 30 DAYS AFTER DELIVERY"
- Create function `extract_payment_details(ocr_data: dict) -> dict`
- Return structured dictionary:
  ```python
  {
    'number_of_payments': int,
    'payment_amount': float,
    'payment_frequency': str
  }
  ```

### Acceptance Criteria
- [ ] All payment fields extracted correctly from sample image
- [ ] Number of payments converted to integer
- [ ] Payment amount converted to float with proper decimal handling

---

## Task 9: Data Extraction Module - Itemization Details
**Priority:** Medium  
**Status:** Pending

### Description
Extract detailed itemization from the "Itemization of Amount Financed" section.

### Requirements
- Extract from `examples/IMG_1805.png`:
  - Cash Price (Includes Tax): "$11,025.60" (as float)
  - Down Payment: "$-" or "$0" (as float, 0.0)
  - Unpaid Balance: "$11,025.60" (as float)
  - Amounts Paid to Others on your behalf: "$-" or "$0" (as float, 0.0)
  - Amount Financed: "$11,025.60" (as float)
- Create function `extract_itemization(ocr_data: dict) -> dict`
- Return structured dictionary:
  ```python
  {
    'cash_price': float,
    'down_payment': float,
    'unpaid_balance': float,
    'amounts_paid_to_others': float,
    'itemized_amount_financed': float
  }
  ```
- Handle negative signs or dashes as zero values

### Acceptance Criteria
- [ ] All itemization fields extracted correctly from sample image
- [ ] Zero/dash values are properly converted to 0.0
- [ ] All amounts are properly formatted as floats

---

## Task 10: Main Extraction Orchestrator
**Priority:** High  
**Status:** Pending

### Description
Create a main function that orchestrates all extraction modules and combines results.

### Requirements
- Create function `extract_all_data(image_path: str) -> dict` that:
  1. Preprocesses the image
  2. Performs OCR extraction
  3. Calls all individual extraction functions
  4. Combines all extracted data into a single dictionary
- Return comprehensive dictionary with all extracted fields:
  ```python
  {
    'seller': {...},
    'buyer': {...},
    'product': {...},
    'financial': {...},
    'payment': {...},
    'itemization': {...},
    'metadata': {
      'source_file': str,
      'extraction_date': str,
      'ocr_confidence': float (optional)
    }
  }
  ```

### Acceptance Criteria
- [ ] Successfully processes `examples/IMG_1805.png`
- [ ] All extraction modules are called in correct order
- [ ] Returns complete, structured data dictionary
- [ ] Includes metadata about extraction process

---

## Task 11: Data Validation Module
**Priority:** High  
**Status:** Pending

### Description
Create validation functions to check extracted data quality and flag potential errors.

### Requirements
- Create function `validate_extracted_data(data: dict) -> dict` that:
  - Validates required fields are present
  - Checks data types (e.g., floats for amounts, ints for counts)
  - Validates phone number formats (basic pattern matching)
  - Validates address formats (basic checks)
  - Cross-validates related fields (e.g., amount financed consistency)
  - Flags missing or suspicious values
- Return validation result dictionary:
  ```python
  {
    'is_valid': bool,
    'errors': list[str],
    'warnings': list[str],
    'validated_data': dict
  }
  ```

### Acceptance Criteria
- [ ] Validates all required fields from sample image
- [ ] Flags missing or invalid data appropriately
- [ ] Provides clear error/warning messages
- [ ] Does not fail silently on validation errors

---

## Task 12: Data Export Module - CSV Format
**Priority:** High  
**Status:** Pending

### Description
Export extracted and validated data to CSV format.

### Requirements
- Create function `export_to_csv(data: dict, output_path: str) -> None`
- Flatten nested dictionary structure into CSV-friendly format
- Create CSV with columns:
  - Seller fields (seller_name, seller_address, seller_phone)
  - Buyer fields (buyer_name, buyer_address, buyer_phone, co_buyer_name, co_buyer_address, co_buyer_phone)
  - Product fields (quantity, items, make_model)
  - Financial fields (apr_percentage, finance_charge, amount_financed, total_of_payments, total_sales_price)
  - Payment fields (number_of_payments, payment_amount, payment_frequency)
  - Itemization fields (cash_price, down_payment, unpaid_balance, amounts_paid_to_others, itemized_amount_financed)
  - Metadata fields (source_file, extraction_date)
- Handle special characters and encoding properly
- Include header row with column names

### Acceptance Criteria
- [ ] Successfully exports data from sample image to CSV
- [ ] CSV is readable in Excel/Google Sheets
- [ ] All fields are properly formatted and escaped
- [ ] CSV structure is clean and ready for manual entry into loan software

---

## Task 13: Data Export Module - Excel Format
**Priority:** Medium  
**Status:** Pending

### Description
Export extracted and validated data to Excel format (.xlsx).

### Requirements
- Create function `export_to_excel(data: dict, output_path: str) -> None`
- Use same column structure as CSV export
- Format Excel file:
  - Header row with bold formatting
  - Proper column widths
  - Number formatting for financial fields (currency, percentages)
  - Date formatting for extraction date
- Create a single worksheet with all data

### Acceptance Criteria
- [ ] Successfully exports data from sample image to Excel
- [ ] Excel file opens correctly in Excel/LibreOffice
- [ ] Formatting is professional and readable
- [ ] All data types are properly formatted (currency, percentages, etc.)

---

## Task 14: Unit Tests for Extraction Functions
**Priority:** High  
**Status:** Pending

### Description
Create comprehensive unit tests for all extraction functions using the sample image.

### Requirements
- Create test file `tests/test_extraction.py`
- Test each extraction function with `examples/IMG_1805.png`:
  - Test seller info extraction
  - Test buyer info extraction
  - Test product info extraction
  - Test financial data extraction
  - Test payment details extraction
  - Test itemization extraction
- Use expected values from the image description:
  - Seller: Passanante's Home Food Service, 1901 Farragut Ave. Bristol, PA 19007, 800-772-7786
  - Buyer: Hannah Hornberse, 500 Ricky Rd Mecheraustury PA 1255, 717-257-0626
  - Co-buyer: Rany Hernberse, 500 Ricky Rd Mecheraustury PA 1255, 717-603-2240
  - Product: Quantity=2, Items=Appliances, Make/Model=Platinum Couture / Cutler
  - Financial: APR=21%, Finance Charge=$3607.72, Amount Financed=$6998, Total Payments=$11,025.76, Total Sales Price=$11,025.76
  - Payment: 48 payments, $229.70 each, Monthly
  - Itemization: Cash Price=$11,025.60, Down Payment=$0, Unpaid Balance=$11,025.60, Amounts Paid to Others=$0, Amount Financed=$11,025.60
- Tests should verify:
  - Correct field extraction
  - Correct data types
  - Handling of edge cases (missing fields, etc.)

### Acceptance Criteria
- [ ] All extraction functions have corresponding tests
- [ ] Tests use actual sample image (`examples/IMG_1805.png`)
- [ ] Tests verify expected values match extracted values
- [ ] Tests handle OCR variations gracefully (fuzzy matching where appropriate)
- [ ] Test suite can be run with `pytest`

---

## Task 15: Integration Test - End-to-End Pipeline
**Priority:** High  
**Status:** Pending

### Description
Create an end-to-end integration test that processes the sample image through the complete pipeline.

### Requirements
- Create test that:
  1. Loads `examples/IMG_1805.png`
  2. Runs complete extraction pipeline
  3. Validates extracted data
  4. Exports to both CSV and Excel
  5. Verifies output files are created and contain expected data
- Test should verify:
  - All major data fields are extracted
  - Data validation passes (or flags appropriate warnings)
  - Export files are generated successfully
  - Exported data matches extracted data

### Acceptance Criteria
- [ ] Complete pipeline runs successfully on sample image
- [ ] All expected data fields are present in output
- [ ] Output files (CSV and Excel) are generated correctly
- [ ] Exported data is accurate and complete

---

## Task 16: Command-Line Interface (CLI)
**Priority:** Medium  
**Status:** Pending

### Description
Create a simple CLI to run the extraction tool.

### Requirements
- Create `main.py` or `cli.py` with command-line interface
- Support command: `python main.py <image_path> [--output-format csv|excel|both] [--output-dir <dir>]`
- Default behavior:
  - Process the image
  - Export to both CSV and Excel in current directory
  - Print extraction summary to console
  - Show validation warnings/errors
- Example usage:
  ```bash
  python main.py examples/IMG_1805.png
  python main.py examples/IMG_1805.png --output-format excel --output-dir ./output
  ```

### Acceptance Criteria
- [ ] CLI successfully processes sample image
- [ ] Output files are created in specified location
- [ ] Console output shows extraction summary
- [ ] Validation results are displayed

---

## Task 17: Error Handling and Logging
**Priority:** Medium  
**Status:** Pending

### Description
Implement comprehensive error handling and logging throughout the application.

### Requirements
- Add logging configuration:
  - Log OCR extraction steps
  - Log extraction results for each field
  - Log validation warnings/errors
  - Log export operations
- Error handling:
  - Handle missing image files gracefully
  - Handle OCR failures with informative messages
  - Handle extraction failures (partial data extraction)
  - Handle export failures
- Create log file for debugging: `extraction.log`

### Acceptance Criteria
- [ ] All major operations are logged
- [ ] Errors are caught and handled gracefully
- [ ] Log file is created and contains useful debugging information
- [ ] User-friendly error messages are displayed

---

## Task 18: Documentation and README
**Priority:** Low  
**Status:** Pending

### Description
Create comprehensive documentation for the PoC.

### Requirements
- Update `README.md` with:
  - Project overview and purpose
  - Setup instructions
  - Usage examples
  - Expected output format
  - Known limitations
  - Testing instructions
- Document the data extraction schema (all fields and their types)
- Include example of expected output

### Acceptance Criteria
- [ ] README is clear and complete
- [ ] Setup instructions work for new users
- [ ] Usage examples are accurate
- [ ] Data schema is documented

---

## Task 19: PoC Validation Against Sample Image
**Priority:** High  
**Status:** Pending

### Description
Final validation that the PoC correctly processes the sample image and produces expected results.

### Requirements
- Run complete pipeline on `examples/IMG_1805.png`
- Verify all extracted values match expected values from image description:
  - All seller, buyer, product, financial, payment, and itemization fields
- Verify output files (CSV and Excel) contain correct data
- Document any discrepancies or OCR limitations encountered
- Create a validation report showing:
  - Extracted values vs. expected values
  - Accuracy percentage for each field category
  - Any fields that require manual review

### Acceptance Criteria
- [ ] PoC successfully processes sample image
- [ ] Extracted data accuracy is documented
- [ ] Output files are ready for client review
- [ ] Known limitations are documented

---

## Notes for Implementation

### Key Considerations
1. **OCR Accuracy**: Handwritten text may have lower OCR accuracy. Consider using multiple OCR engines or post-processing to improve results.
2. **Layout Parsing**: The document has a structured layout. Use coordinate-based parsing to locate fields by their position relative to labels.
3. **Data Validation**: Some fields may be ambiguous (e.g., handwritten numbers). Flag these for manual review rather than guessing.
4. **Testing**: All tests should use the actual sample image (`examples/IMG_1805.png`) to ensure real-world accuracy.
5. **Extensibility**: Design the code to be easily extended for processing multiple documents in the future.

### Expected Challenges
- Handwritten text recognition accuracy
- Parsing currency values with commas and dollar signs
- Handling variations in field positions
- Distinguishing between similar-looking characters (e.g., "0" vs "O", "1" vs "l")

### Success Criteria for PoC
- Successfully extracts at least 90% of fields correctly from the sample image
- Produces clean, structured output ready for manual review/entry
- Demonstrates the approach is viable for scaling to multiple documents
- Code is maintainable and well-documented

