"""
TMS Bulk - Convert CSV to XLSX
"""

# Imports
import json
import pandas as pd
from tqdm import tqdm

# Utils Functions


# Main Functions
def TMSBulk_Convert_CSV_to_XLSX(CSV_PATH, XLSX_PATH):
    '''
    TMS Bulk - Convert CSV data to XLSX format
    '''
    DF = pd.read_csv(CSV_PATH, keep_default_na=False, na_values=[])
    DF.to_excel(XLSX_PATH, index=False)

# Main Vars
PATHS = {
    "input": {
        "path": "Data/BulkTranslationHelper/Data/Temp/input/input.csv",
    },
    "output": {
        "path": "Data/BulkTranslationHelper/Data/Temp/output/output.xlsx"
    }
}

OPERATION_FROM = "csv"
OPERATION_TO = "xlsx"

# Run Code Functions
def run():
    print(f"Reading {OPERATION_FROM}: {PATHS['input']['path']}")

    TMSBulk_Convert_CSV_to_XLSX(PATHS["input"]["path"], PATHS["output"]["path"])

    print(f"Conversion Complete. {OPERATION_TO} data saved to {PATHS['output']['path']}")

# Run Code
if __name__ == "__main__":
    run()