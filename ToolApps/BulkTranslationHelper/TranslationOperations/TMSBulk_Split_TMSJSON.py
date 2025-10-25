"""
TMS Bulk - Split TMS JSON

Operation: Splits joint TMS JSON into separate JSONs for each locale

Input:
{
    "en": {
        "mobile": {
            "mobile_test": 1
        }
    },
    "de": {
        "number": {
            "number_test": 1
        }
    }
}

Output:
en.json
{
    "mobile": {
        "mobile_test": 1
    }
}
de.json
{
    "number": {
        "number_test": 1
    }
}
"""

# Imports
import os
import json
from tqdm import tqdm

# Utils Functions


# Main Functions


# Main Vars
PATHS = {
    "input": {
        "path": "Data/BulkTranslationHelper/Data/Temp/input/input.json"
    },
    "output": {
        "dir": "Data/BulkTranslationHelper/Data/Temp/output/",
        "prefix": "output_"
    }
}

OPERATION_FROM = "json"
OPERATION_TO = "json"

# Run Code Functions
def run():
    ## Read JSON
    print(f"Reading {OPERATION_FROM} and splitting...")

    JOINT_JSON = json.load(open(PATHS["input"]["path"], "r"))

    for lang in tqdm(JOINT_JSON):
        SAVE_SPLIT_JSON_PATH = os.path.join(PATHS["output"]["dir"], f"{PATHS['output']['prefix']}{lang}.json")
        SPLIT_JSON = JOINT_JSON[lang]
        json.dump(SPLIT_JSON, open(SAVE_SPLIT_JSON_PATH, "w"), ensure_ascii=False, indent=4)

    print(f"Split Complete. {OPERATION_TO} data saved to {PATHS['output']['dir']}")

# Run Code
if __name__ == "__main__":
    run()