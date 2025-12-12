# Finance Agreement Data Extraction PoC

A Proof of Concept (PoC) tool to extract structured data from scanned finance agreement documents. This tool utilizes OCR (Optical Character Recognition) and spatial analysis to parse key information such as Seller, Buyer, Product, Financial, and Payment details, even from rotated images.

## Features

- **Robust Preprocessing**: Handles image denoising, binarization, and grayscale conversion.
- **Advanced OCR Integration**: Uses Tesseract 5 with layout analysis to detect text blocks.
- **Spatial Parsing Engine**: Custom logic to handle document rotation (90-degree text) and multi-column layouts.
- **Data Validation**: Checks for critical fields and validates data types (currency, dates).
- **Multi-Format Export**: Generates:
  - **JSON**: Complete hierarchical data structure.
  - **CSV**: Flattened data for database import.
  - **Excel (.xlsx)**: Formatted spreadsheet for business review.
- **CLI Interface**: Easy-to-use command line tool for batch processing.

## Prerequisites

- **Python**: 3.8+
- **Tesseract OCR**: Must be installed on the system.
  - **macOS**: `brew install tesseract`
  - **Ubuntu**: `sudo apt-get install tesseract-ocr`
  - **Windows**: [Download Installer](https://github.com/UB-Mannheim/tesseract/wiki)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd matt-rappoport-poc
   ```

2. **Create a virtual environment** (Optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool using the Command Line Interface (CLI):

```bash
python3 cli.py <image_path> [options]
```

### Examples

**Process a single image and export to default locations (current dir):**
```bash
python3 cli.py examples/IMG_1805.png
```

**Export only to Excel in a specific folder:**
```bash
python3 cli.py examples/IMG_1805.png --output-format excel --output-dir ./results
```

### Options

- `image_path`: Path to the input image file (Required).
- `--output-format`: Output file format. Choices: `csv`, `excel`, `both`. Default: `both`.
- `--output-dir`: Directory to save the output files. Default: `.` (current directory).

## Data Schema

The tool extracts the following fields:

### Seller Information
- `seller_name` (Text)
- `seller_address` (Text)
- `seller_phone` (Text)

### Buyer Information
- `buyer_name` (Text)
- `buyer_address` (Text)
- `buyer_phone` (Text)

### Product Information
- `quantity` (Text/Int)
- `items` (Text)
- `make_model` (Text)

### Financial Data
- `apr_percentage` (Float, e.g., 21.0)
- `finance_charge` (Float)
- `amount_financed` (Float)
- `total_of_payments` (Float)
- `total_sales_price` (Float)

### Payment Schedule
- `number_of_payments` (Int)
- `payment_amount` (Float)
- `payment_frequency` (Text, e.g., "Monthly")

### Itemization
- `cash_price` (Float)
- `down_payment` (Float)
- `unpaid_balance` (Float)
- `amounts_paid_to_others` (Float)
- `itemized_amount_financed` (Float)

## Project Structure

```
.
├── src/
│   ├── extractor.py    # OCR interface (Tesseract wrapper)
│   ├── parser.py       # Core logic for text extraction & regex
│   ├── preprocessor.py # Image cleaning (OpenCV)
│   ├── validator.py    # Data integrity checks
│   ├── exporter.py     # CSV/Excel generation
│   ├── pipeline.py     # Orchestrator
│   └── logger.py       # Logging config
├── tests/              # Unit and Integration tests
├── examples/           # Sample images
├── cli.py              # CLI entry point
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Testing

Run the automated test suite using `pytest`:

```bash
# Run all tests
python3 -m pytest tests/

# Run integration tests only
python3 -m pytest tests/test_integration.py
```

## Capabilities & Limitations

- **Rotation Handling**: The system is tuned to handle the 90-degree rotation observed in the sample data (`IMG_1805.png`).
- **Handwriting**: Tesseract (the open-source OCR engine execution) has limited accuracy with cursive handwriting. Fields like "Buyer Name" may contain OCR artifacts (e.g., "sran" instead of "Hannah").
    - **Recommendation**: For production use with handwritten forms, consider integrating a cloud-based AI OCR service (AWS Textract, Google Cloud Vision) or a fine-tuned handwriting model. The extraction architecture (`Parser` class) is agnostic and can easily adapt to better OCR inputs.

## License

[License Name]
