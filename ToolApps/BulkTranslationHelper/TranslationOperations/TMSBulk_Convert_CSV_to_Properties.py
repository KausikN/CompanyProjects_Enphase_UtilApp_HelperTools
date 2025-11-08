"""
TMS Bulk - Convert CSV to Properties
"""

# Imports
import json
import pandas as pd
from tqdm import tqdm

# Utils Functions


# Main Functions
def TMSBulk_Convert_CSV_to_Props(CSV_PATH, PROPS_DIR_PATH, PROPS_PATH_PREFIX=""):
    '''
    TMS Bulk - Convert CSV data to Properties format
    '''
    # Read CSV File
    DF = pd.read_csv(CSV_PATH, keep_default_na=False, na_values=[])
    LOCALES = [c for c in DF.columns if c not in ["key"]]
    
    # Convert to Properties and Save
    for locale in LOCALES:
        props_lines = []
        for _, row in DF.iterrows():
            key = row["key"]
            value = row[locale]
            props_lines.append(f"{key}={value}")
        props_content = "\n".join(props_lines)
        props_file_path = f"{PROPS_DIR_PATH}/{PROPS_PATH_PREFIX}{locale}.properties"
        with open(props_file_path, "w", encoding="utf-8") as props_file:
            props_file.write(props_content)

# Main Vars
PATHS = {
    "input": {
        "path": "Data/BulkTranslationHelper/Data/Temp/input/input.csv",
    },
    "output": {
        "dir": "Data/BulkTranslationHelper/Data/Temp/output/",
        "prefix": "output_",
    }
}

OPERATION_FROM = "csv"
OPERATION_TO = "properties"

# Run Code Functions
def run():
    print(f"Reading {OPERATION_FROM}: {PATHS['input']['path']}")

    TMSBulk_Convert_CSV_to_Props(PATHS["input"]["path"], PATHS["output"]["dir"], PATHS["output"]["prefix"])

    print(f"Conversion Complete. {OPERATION_TO} data saved to {PATHS['output']['dir']}")

# Run Code
if __name__ == "__main__":
    run()