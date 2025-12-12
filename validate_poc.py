import os
import sys
from datetime import datetime

# Ensure src can be imported
sys.path.append(os.getcwd())

from src.pipeline import extract_all_data

# Expected Values (Ground Truth for IMG_1805.png)
# Based on visual inspection and known OCR limitations.
EXPECTED = {
    'seller': {
        'seller_name': 'RAINBOW VACUUM SALES & SERVICE',
        'seller_phone': '800-772-7786',
        # Address matching is fuzzy due to multi-line joins
        'seller_address_partial': '1901 Farragut Ave' 
    },
    'buyer': {
        # Handwriting - Expecting poor results or empty
        'buyer_name_check': lambda x: x is not None, 
        'buyer_address_check': lambda x: x is not None
    },
    'financial': {
        'apr_percentage': 21.0,
        'finance_charge': 279.34, 
        'amount_financed': 900.00,
        'total_of_payments': 1179.34,
        'total_sales_price': 1229.34 # 1179.34 + 50.00 down? or similar
    },
    'payment': {
        'payment_amount': 24.57,
        'number_of_payments': 48,
        'payment_frequency_partial': 'Monthly'
    },
    'product': {
        'items_partial': 'Appliances',
        'make_model_partial': 'Platinum'
    }
}

def validate_field(actual, expected, field_name):
    if expected is None:
        return "SKIP"
    
    # Callable check
    if callable(expected):
        return "PASS" if expected(actual) else "FAIL"
        
    # Text Partial Match
    if field_name.endswith('_partial'):
        if actual and expected.lower() in actual.lower():
            return "PASS"
        return "FAIL"
        
    # Float precision match
    if isinstance(expected, float):
        if actual is None:
            return "FAIL"
        if abs(actual - expected) < 0.01:
            return "PASS"
        return "FAIL"
        
    # Exact match
    if actual == expected:
        return "PASS"
        
    return "FAIL"

def run_validation(image_path):
    print(f"Validating {image_path}...")
    
    try:
        data = extract_all_data(image_path)
    except Exception as e:
        print(f"CRITICAL: Pipeline crashed - {e}")
        return
        
    report_lines = []
    report_lines.append(f"# Validation Report: {os.path.basename(image_path)}")
    report_lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report_lines.append("")
    report_lines.append("| Category | Field | Expected | Actual | Status |")
    report_lines.append("|---|---|---|---|---|")
    
    categories = ['seller', 'buyer', 'financial', 'payment', 'product']
    
    total_checks = 0
    passed_checks = 0
    
    for cat in categories:
        rules = EXPECTED.get(cat, {})
        actual_data = data.get(cat, {})
        
        for key, expected_val in rules.items():
            # Handle special key names
            real_key = key.replace('_partial', '').replace('_check', '')
            actual_val = actual_data.get(real_key)
            
            status = validate_field(actual_val, expected_val, key)
            
            # Formatting for table
            disp_expected = str(expected_val) if not callable(expected_val) else "Check logic"
            disp_actual = str(actual_val)
            
            icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
            
            report_lines.append(f"| {cat.capitalize()} | {real_key} | {disp_expected} | {disp_actual} | {icon} {status} |")
            
            if status != "SKIP":
                total_checks += 1
                if status == "PASS":
                    passed_checks += 1

    accuracy = (passed_checks / total_checks * 100) if total_checks > 0 else 0
    report_lines.append("")
    report_lines.append(f"**Overall Accuracy:** {accuracy:.1f}% ({passed_checks}/{total_checks})")
    
    # Write report
    with open("validation_report.md", "w") as f:
        f.write("\n".join(report_lines))
        
    print(f"Validation Complete. Report written to 'validation_report.md'. Accuracy: {accuracy:.1f}%")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_poc.py <image_path>")
        sys.exit(1)
        
    run_validation(sys.argv[1])
