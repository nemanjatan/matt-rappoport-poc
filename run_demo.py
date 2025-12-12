from src.pipeline import extract_all_data
from src.validator import validate_extracted_data
from src.exporter import export_to_csv, export_to_excel
import json
import os

def main():
    image_path = "examples/IMG_1805.png"
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found.")
        return

    print(f"Processing {image_path}...")
    
    # 1. Pipeline Extraction
    extracted_data = extract_all_data(image_path)
    print("Extraction successful.")
    
    # 2. Validation
    validation_result = validate_extracted_data(extracted_data)
    if validation_result['is_valid']:
        print("Validation Passed.")
    else:
        print("Validation Failed.")
        print("Errors:", validation_result['errors'])
    
    if validation_result['warnings']:
        print("Warnings:", validation_result['warnings'])
        
    # 3. Export
    # Save JSON for inspection
    with open("output.json", "w") as f:
        json.dump(extracted_data, f, indent=2)
    print("Saved output.json")
    
    # Export CSV
    export_to_csv(extracted_data, "output.csv")
    print("Saved output.csv")
    
    # Export Excel
    export_to_excel(extracted_data, "output.xlsx")
    print("Saved output.xlsx")
    
    print("\n------------------------------------------------")
    print("PoC Demo Complete.")
    print("Check output.csv and output.xlsx for results.")

if __name__ == "__main__":
    main()
