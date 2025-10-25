"""
TMS Bulk - Convert JSON to YML
"""

# Imports
import json
import yaml
from tqdm import tqdm

# Utils Functions


# Main Functions
def TMSBulk_Convert_JSON_to_YML(JSON_PATH, YML_PATH):
    '''
    TMS Bulk - Convert JSON data to YML format
    '''
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(YML_PATH, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)

# Main Vars
PATHS = {
    "input": {
        "path": "Data/BulkTranslationHelper/Data/Temp/input/input.json"
    },
    "output": {
        "path": "Data/BulkTranslationHelper/Data/Temp/output/output.yml"
    }
}

OPERATION_FROM = "json"
OPERATION_TO = "yml"

# Run Code Functions
def run():
    print(f"Reading {OPERATION_FROM}: {PATHS['input']['path']}")

    TMSBulk_Convert_JSON_to_YML(PATHS["input"]["path"], PATHS["output"]["path"])

    print(f"Conversion Complete. {OPERATION_TO} data saved to {PATHS['output']['path']}")

# Run Code
if __name__ == "__main__":
    run()