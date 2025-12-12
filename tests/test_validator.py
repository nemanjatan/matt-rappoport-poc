import pytest
from src.validator import validate_extracted_data

def test_validate_extracted_data_valid():
    mock_data = {
        'seller': {'seller_name': 'Valid Seller'},
        'financial': {'finance_charge': 100.0, 'amount_financed': 500.0},
        'payment': {'payment_amount': 50.0, 'number_of_payments': 10},
        'buyer': {'buyer_name': 'John Doe'}
    }
    result = validate_extracted_data(mock_data)
    assert result['is_valid'] is True
    assert len(result['errors']) == 0
    assert len(result['warnings']) == 0

def test_validate_extracted_data_missing_critical():
    mock_data = {
        'seller': {'seller_name': ''}, # Missing name
        'financial': {},
        'payment': {}
    }
    result = validate_extracted_data(mock_data)
    assert result['is_valid'] is False
    assert "Missing required field: Seller Name" in result['errors']

def test_validate_extracted_data_warnings():
    # Valid structure but missing non-critical (warning) fields
    mock_data = {
        'seller': {'seller_name': 'Valid Seller'},
        'financial': {'finance_charge': None}, # Warning
        'payment': {'payment_amount': None}, # Warning
        'buyer': {} # Warning
    }
    result = validate_extracted_data(mock_data)
    assert result['is_valid'] is True # Still accessible
    assert len(result['warnings']) > 0
    assert "Finance Charge not extracted or invalid." in result['warnings']
