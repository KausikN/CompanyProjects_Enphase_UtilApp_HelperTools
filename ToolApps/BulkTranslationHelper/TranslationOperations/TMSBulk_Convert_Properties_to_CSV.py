"""
TMS Bulk - Convert Properties to CSV
"""

# Imports
import json
import pandas as pd
from tqdm import tqdm

# Utils Functions


# Main Functions
def TMSBulk_Convert_Props_to_CSV(PROPS_PATH, CSV_PATH, value_column_name="en"):
    '''
    TMS Bulk - Convert Properties data to CSV format
    '''
    # Read Properties File
    props_data = {}
    with open(PROPS_PATH, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key_value = line.split('=', 1)
                if len(key_value) == 2:
                    key, value = key_value
                    props_data[key.strip()] = value.strip()
    # Convert to DataFrame
    df = pd.DataFrame(list(props_data.items()), columns=["key", value_column_name])
    # Save to CSV
    df.to_csv(CSV_PATH, index=False)

# Main Vars
PATHS = {
    "input": {
        "path": "Data/BulkTranslationHelper/Data/Temp/input/input.properties",
    },
    "output": {
        "path": "Data/BulkTranslationHelper/Data/Temp/output/output.csv",
    }
}

OPERATION_FROM = "properties"
OPERATION_TO = "csv"
VALUE_COLUMN_NAME = "value"

# Run Code Functions
def run():
    print(f"Reading {OPERATION_FROM}: {PATHS['input']['path']}")

    TMSBulk_Convert_Props_to_CSV(PATHS["input"]["path"], PATHS["output"]["path"], VALUE_COLUMN_NAME)

    print(f"Conversion Complete. {OPERATION_TO} data saved to {PATHS['output']['path']}")

# Run Code
if __name__ == "__main__":
    run()