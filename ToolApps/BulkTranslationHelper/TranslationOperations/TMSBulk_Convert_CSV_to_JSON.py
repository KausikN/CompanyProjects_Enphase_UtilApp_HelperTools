"""
TMS Bulk - Convert CSV to JSON
"""

# Imports
from .TMSBulk_Library_Convert import *

# Main Vars
PREFIXES = {
    "none": [],
    "e_i18n": [
        "mobile.",
        "date.",
        "consumer.",
        "number.",
        "time."
    ],
    "battery_profile_ui": ["bp"]
}

PATHS = {
    "input": {
        "path": "Data/BulkTranslationHelper/Data/Temp/input/input.csv"
    },
    "output": {
        "path": "Data/BulkTranslationHelper/Data/Temp/output/output.json"
    }
}

OPERATION_FROM = "csv"
OPERATION_TO = "json"

PREFIX_FILTER_PARAMS = {
    # e_i18n
    # "prefixes": PREFIXES["e_i18n"],
    # "negative_filter": False

    # battery_profile_ui
    # "prefixes": PREFIXES["battery_profile_ui"],
    # "negative_filter": False

    # None
    "prefixes": PREFIXES["none"],
    "negative_filter": True
}

# Run Code Functions
def run():
    # CSV to JSON Conversion
    ## Reading CSV
    print(f"Reading {OPERATION_FROM}: {PATHS['input']['path']}")
    CSV_DATA = pd.read_csv(PATHS["input"]["path"], keep_default_na=False, na_values=[])
    print("CSV Sample:")
    print(CSV_DATA.head())
    print()
    ## Apply Filters
    Print_CSVMetadata(CSV_DATA, header=" --- Original CSV Data ---")
    # CSV_DATA = TMSBulk_Filter_ArrayKeys(CSV_DATA, negative_filter=True)
    Print_CSVMetadata(CSV_DATA, header=" --- After Array Key Filter --- ")
    # CSV_DATA = TMSBulk_Filter_PrefixesFilter(CSV_DATA, **PREFIX_FILTER_PARAMS)
    Print_CSVMetadata(CSV_DATA, header=" --- After Prefixes Filter --- ")
    ## Conversion
    JSON_DATA = TMSBulk_Convert_CSV_to_JSON(CSV_DATA)
    ## Save JSON
    with open(PATHS["output"]["path"], "w", encoding="utf-8") as json_file: json.dump(JSON_DATA, json_file, ensure_ascii=False, indent=4)
    print(f"Conversion Complete. {OPERATION_TO} data saved to {PATHS['output']['path']}")

# Run Code
if __name__ == "__main__":
    run()