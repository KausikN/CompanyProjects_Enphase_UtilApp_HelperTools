"""
TMS Bulk - Combined Operations
"""

# Imports
import os
import json
from tqdm import tqdm

from . import TMSBulk_Clean_TMSJSON
from . import TMSBulk_Join_TMSJSON
from . import TMSBulk_Split_TMSJSON
from . import TMSBulk_Convert_CSV_to_JSON
from . import TMSBulk_Convert_CSV_to_Properties
from . import TMSBulk_Convert_CSV_to_XLSX
from . import TMSBulk_Convert_JSON_to_CSV
from . import TMSBulk_Convert_JSON_to_YML
from . import TMSBulk_Convert_Properties_to_CSV
from . import TMSBulk_Convert_YML_to_JSON

# Main Vars


# Main Functions
def TMSBulk_CombinedOperation_YML_to_XLSX(YML_PATH, XLSX_PATH, temp_dir="", temp_prefix=""):
    '''
    TMS Bulk - Combined Operation - YML to XLSX
    '''
    # YML to JSON
    print("--- CONVERT YML to JSON ---")
    YML_to_JSON = TMSBulk_Convert_YML_to_JSON
    TEMP_PATH_JSON = os.path.join(temp_dir, f"{temp_prefix}.json")
    YML_to_JSON.PATHS.update({
        "input": {
            "path": YML_PATH
        },
        "output": {
            "path": TEMP_PATH_JSON
        }
    })
    YML_to_JSON.run()
    print("--- CONVERT YML to JSON ---")

    # JSON to CSV
    print("--- CONVERT JSON to CSV ---")
    JSON_to_CSV = TMSBulk_Convert_JSON_to_CSV
    TEMP_PATH_CSV = os.path.join(temp_dir, f"{temp_prefix}.csv")
    JSON_to_CSV.PATHS.update({
        "input": {
            "path": TEMP_PATH_JSON
        },
        "output": {
            "path": TEMP_PATH_CSV
        }
    })
    JSON_to_CSV.run()
    print("--- CONVERT JSON to CSV ---")

    # CSV to XLSX
    print("--- CONVERT CSV to XLSX ---")
    CSV_to_XLSX = TMSBulk_Convert_CSV_to_XLSX
    CSV_to_XLSX.PATHS.update({
        "input": {
            "path": TEMP_PATH_CSV
        },
        "output": {
            "path": XLSX_PATH
        }
    })
    CSV_to_XLSX.run()
    print("--- CONVERT CSV to XLSX ---")

# Main Vars
PATHS = {
    "input": {
        "path": "Data/BulkTranslationHelper/Data/Temp/input/input.yml"
    },
    "output": {
        "path": "Data/BulkTranslationHelper/Data/Temp/output/output.xlsx"
    },
    "temp": {
        "dir": "Data/BulkTranslationHelper/Data/Temp/output/",
        "prefix": "temp_"
    }
}

# Run Code Functions
def run():
    TMSBulk_CombinedOperation_YML_to_XLSX(PATHS["input"]["path"], PATHS["output"]["path"], PATHS["temp"]["dir"], PATHS["temp"]["prefix"])

# Run Code
if __name__ == "__main__":
    run()