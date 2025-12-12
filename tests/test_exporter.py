import pytest
import os
import csv
from src.exporter import export_to_csv

def test_export_to_csv():
    # Mock data
    mock_data = {
        'seller': {'seller_name': 'Test Seller', 'seller_phone': '555-0101'},
        'buyer': {'buyer_name': 'Test Buyer'},
        'financial': {'finance_charge': 123.45},
        'metadata': {'source_file': 'test.png'}
    }
    
    output_path = "test_output.csv"
    if os.path.exists(output_path):
        os.remove(output_path)
        
    export_to_csv(mock_data, output_path)
    
    assert os.path.exists(output_path)
    
    with open(output_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    assert len(rows) == 1
    row = rows[0]
    assert row['seller_name'] == 'Test Seller'
    assert row['finance_charge'] == '123.45'
    
    # Cleanup
    os.remove(output_path)
