"""
TMS Bulk - Convert YML to JSON
"""

# Imports
import json
import yaml
from tqdm import tqdm

# Utils Functions


# Main Functions
def TMSBulk_Convert_YML_to_JSON(YML_PATH, JSON_PATH):
    '''
    TMS Bulk - Convert YML data to XLSX JSON
    '''
    with open(YML_PATH, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Main Vars
PATHS = {
    "input": {
        "path": "Data/BulkTranslationHelper/Data/Temp/input/input.yml"
    },
    "output": {
        "path": "Data/BulkTranslationHelper/Data/Temp/output/output.json"
    }
}

OPERATION_FROM = "yml"
OPERATION_TO = "json"

# Run Code Functions
def run():
    print(f"Reading {OPERATION_FROM}: {PATHS['input']['path']}")

    TMSBulk_Convert_YML_to_JSON(PATHS["input"]["path"], PATHS["output"]["path"])

    print(f"Conversion Complete. {OPERATION_TO} data saved to {PATHS['output']['path']}")

# Run Code
if __name__ == "__main__":
    run()