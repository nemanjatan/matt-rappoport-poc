import re
from src.logger import setup_logger

logger = setup_logger()

def validate_extracted_data(data: dict) -> dict:
    """
    Validates the structure and content of the extracted data.
    
    Returns:
        {
            'is_valid': bool,
            'errors': list[str],
            'warnings': list[str],
            'validated_data': dict
        }
    """
    logger.debug("Starting data validation")
    errors = []
    warnings = []
    
    # 1. Critical Fields (fail if missing)
    seller = data.get('seller', {})
    if not seller or not seller.get('seller_name'):
        msg = "Missing required field: Seller Name"
        errors.append(msg)
        logger.error(msg)
        
    # 2. Financial Data Checks (warnings if missing/invalid)
    financial = data.get('financial', {})
    if financial.get('finance_charge') is None:
        warnings.append("Finance Charge not extracted or invalid.")
    elif not isinstance(financial.get('finance_charge'), (float, int)):
        warnings.append(f"Finance Charge has invalid type: {type(financial.get('finance_charge'))}")
        
    # Check consistency: Amount Financed
    if financial.get('amount_financed') is None:
        warnings.append("Amount Financed not extracted.")

    # 3. Payment Details
    payment = data.get('payment', {})
    if payment.get('payment_amount') is None:
        warnings.append("Payment Amount not extracted.")
    elif not isinstance(payment.get('payment_amount'), (float, int)):
        warnings.append("Payment Amount has invalid type.")
        
    if payment.get('number_of_payments') is None:
        warnings.append("Number of Payments not extracted.")

    # 4. Buyer Info (Warning if completely empty)
    buyer = data.get('buyer', {})
    if not buyer.get('buyer_name') and not buyer.get('buyer_address'):
        warnings.append("Buyer Information appears empty.")

    # Determine overall validity (Errors blocks usage, Warnings do not)
    is_valid = len(errors) == 0
    
    if is_valid:
        logger.info("Validation passed")
    else:
        logger.error(f"Validation failed with {len(errors)} errors")
        
    if warnings:
        logger.warning(f"Validation produced {len(warnings)} warnings")

    return {
        'is_valid': is_valid,
        'errors': errors,
        'warnings': warnings,
        'validated_data': data
    }
