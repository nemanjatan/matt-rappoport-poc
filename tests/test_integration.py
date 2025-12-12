import pytest
import os
import csv
import openpyxl
from src.pipeline import extract_all_data
from src.validator import validate_extracted_data
from src.exporter import export_to_csv, export_to_excel

IMG_PATH = "examples/IMG_1805.png"
CSV_OUT = "test_full_output.csv"
XLSX_OUT = "test_full_output.xlsx"

@pytest.fixture(autouse=True)
def cleanup():
    # Setup: Remove old files
    if os.path.exists(CSV_OUT):
        os.remove(CSV_OUT)
    if os.path.exists(XLSX_OUT):
        os.remove(XLSX_OUT)
    yield
    # Teardown: Remove generated files
    if os.path.exists(CSV_OUT):
        os.remove(CSV_OUT)
    if os.path.exists(XLSX_OUT):
        os.remove(XLSX_OUT)

def test_end_to_end_pipeline():
    if not os.path.exists(IMG_PATH):
        pytest.skip(f"Test image not found at {IMG_PATH}")
        
    # 1. Extraction
    print("Running Extraction...")
    data = extract_all_data(IMG_PATH)
    assert data is not None
    assert 'seller' in data
    
    # 2. Validation
    print("Running Validation...")
    report = validate_extracted_data(data)
    # Ideally should be valid, or valid with recognized warnings
    assert report['is_valid'] is True, f"Validation failed with errors: {report['errors']}"
    
    # 3. Export CSV
    print("Exporting CSV...")
    export_to_csv(data, CSV_OUT)
    assert os.path.exists(CSV_OUT)
    
    # Verify CSV Content
    with open(CSV_OUT, 'r') as f:
        content = f.read()
        assert "Passanante" in content
        # Check for financial charge 3667.22 (known OCR value)
        assert "3667.22" in content
        
    # 4. Export Excel
    print("Exporting Excel...")
    export_to_excel(data, XLSX_OUT)
    assert os.path.exists(XLSX_OUT)
    
    # Verify Excel Content
    wb = openpyxl.load_workbook(XLSX_OUT)
    ws = wb.active
    # Simple check if data row exists
    assert ws.max_row >= 2
    wb.close()
    
    print("End-to-End Test Completed Successfully.")
