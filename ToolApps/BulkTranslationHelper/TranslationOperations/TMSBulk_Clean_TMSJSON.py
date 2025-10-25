"""
TMS Bulk - Clean TMS JSON of format

Operation: Picks out only the non "en" locale key

Input:
{
    "en": {
        "test_en": 1
    },
    "sv": {
        "test_sv": 1
    }
}

Output:
{
    "test_sv": 1
}
"""

# Imports
import json
from tqdm import tqdm

# Utils Functions


# Main Functions
def TMSBulk_Clean_TMSJSON(JSON_DATA):
    '''
    TMS Bulk - Clean TMS JSON
    '''
    LOCALE = [l for l in list(JSON_DATA.keys()) if l not in ["en"]][0]
    CLEANED_JSON_DATA = JSON_DATA[LOCALE]

    return CLEANED_JSON_DATA

# Main Vars
PATHS = {
    "input": {
        "path": "Data/BulkTranslationHelper/Data/Temp/input/input.json"
    },
    "output": {
        "path": "Data/BulkTranslationHelper/Data/Temp/output/output.json"
    }
}

OPERATION_FROM = "json"
OPERATION_TO = "json"

# Run Code Functions
def run():
    print(f"Reading {OPERATION_FROM}: {PATHS['input']['path']}")

    with open(PATHS["input"]["path"], "r", encoding="utf-8") as json_file: JSON_DATA = json.load(json_file)

    CLEANED_JSON_DATA = TMSBulk_Clean_TMSJSON(JSON_DATA)

    with open(PATHS["output"]["path"], 'w', encoding='utf-8') as f: json.dump(CLEANED_JSON_DATA, f, ensure_ascii=False, indent=4)

    print(f"Clean Complete. {OPERATION_TO} data saved to {PATHS['output']['path']}")

# Run Code
if __name__ == "__main__":
    run()