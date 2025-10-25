"""
TMS Bulk - Join TMS JSON

Operation: Joins multiple JSONs

Input:
en/mobile.json
{
    "mobile_test": 1
}
de/number.json
{
    "number_test": 1
}

Output:
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
"""

# Imports
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
        "path": "Data/BulkTranslationHelper/Data/Temp/output/output.json"
    }
}

OPERATION_FROM = "json"
OPERATION_TO = "json"

LOCALE_JOIN_PATHS = {
    "en": {
        "consumer": "Data/en/consumer.json",
        "date": "Data/en/date.json",
        "mobile": "Data/en/mobile.json",
        "number": "Data/en/number.json",
        "time": "Data/en/time.json"
    }
}

# Run Code Functions
def run():
    ## Read JSONs
    print(f"Reading {OPERATION_FROM} and joining...")

    JOINT_JSON = {}

    for lang in tqdm(LOCALE_JOIN_PATHS):
        JOINT_JSON[lang] = {}
        for k in LOCALE_JOIN_PATHS[lang]:
            JOINT_JSON[lang][k] = json.load(open(LOCALE_JOIN_PATHS[lang][k], "r"))

    ## Write Joint JSON
    json.dump(JOINT_JSON, open(PATHS["output"]["path"], "w"), ensure_ascii=False, indent=4)

    print(f"Join Complete. {OPERATION_TO} data saved to {PATHS['output']['path']}")

# Run Code
if __name__ == "__main__":
    run()