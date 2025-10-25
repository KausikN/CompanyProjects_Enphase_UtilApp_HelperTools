"""
TMS Bulk - Convert JSON to CSV
"""

# Imports
from .TMSBulk_Library_Convert import *

# Main Vars
PATHS = {
    "input": {
        "path": "Data/BulkTranslationHelper/Data/Temp/input/input.json"
    },
    "output": {
        "path": "Data/BulkTranslationHelper/Data/Temp/output/output.csv"
    }
}

OPERATION_FROM = "json"
OPERATION_TO = "csv"

# Run Code Functions
def run():
    # JSON to CSV Conversion
    ## Reading JSON
    print(f"Reading {OPERATION_FROM}: {PATHS['input']['path']}")
    with open(PATHS["input"]["path"], "r", encoding="utf-8") as json_file: JSON_DATA = json.load(json_file)
    print("{OPERATION_FROM} Sample:")
    print(json.dumps(JSON_DATA, ensure_ascii=False, indent=4)[:100] + "...")
    print()
    ## Conversion
    CSV_DATA = TMSBulk_Convert_JSON_to_CSV(JSON_DATA)
    Print_CSVMetadata(CSV_DATA, header=" --- Converted Output Data --- ")
    ## Save CSV
    CSV_DATA.to_csv(PATHS["output"]["path"], index=False)
    print(f"Conversion Complete. {OPERATION_TO} data saved to {PATHS['output']['path']}")

# Run Code
if __name__ == "__main__":
    run()