import argparse
import os
import sys

# Ensure src can be imported if running from root
sys.path.append(os.getcwd())

from src.pipeline import extract_all_data
from src.validator import validate_extracted_data
from src.exporter import export_to_csv, export_to_excel

def main():
    parser = argparse.ArgumentParser(description="Extract data from finance agreement images.")
    parser.add_argument("image_path", help="Path to the input image file.")
    parser.add_argument("--output-format", choices=['csv', 'excel', 'both'], default='both', help="Output format (default: both).")
    parser.add_argument("--output-dir", default=".", help="Directory to save output files (default: current directory).")
    
    args = parser.parse_args()
    
    # Validation of input
    if not os.path.exists(args.image_path):
        print(f"Error: Input file '{args.image_path}' not found.")
        sys.exit(1)
        
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        print(f"Created output directory: {args.output_dir}")

    print(f"Processing: {args.image_path}")
    print("-" * 40)

    try:
        # 1. Extract
        print("Step 1: Extracting data...")
        data = extract_all_data(args.image_path)
        
        # 2. Validate
        print("Step 2: Validating data...")
        report = validate_extracted_data(data)
        
        if report['is_valid']:
            print("Validation: PASSED")
        else:
            print("Validation: FAILED")
            for err in report['errors']:
                print(f"  [ERROR] {err}")
            # Depending on policy, we might exit here. For PoC, we proceed but warn.
            print("Warning: Proceeding with export despite validation errors.")
            
        if report['warnings']:
            for warn in report['warnings']:
                print(f"  [WARNING] {warn}")
        
        # 3. Export
        base_name = os.path.splitext(os.path.basename(args.image_path))[0]
        
        if args.output_format in ['csv', 'both']:
            out_csv = os.path.join(args.output_dir, f"{base_name}_extracted.csv")
            export_to_csv(data, out_csv)
            print(f"Exported CSV: {out_csv}")
            
        if args.output_format in ['excel', 'both']:
            out_xlsx = os.path.join(args.output_dir, f"{base_name}_extracted.xlsx")
            export_to_excel(data, out_xlsx)
            print(f"Exported Excel: {out_xlsx}")
            
        print("-" * 40)
        print("Processing Complete.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
