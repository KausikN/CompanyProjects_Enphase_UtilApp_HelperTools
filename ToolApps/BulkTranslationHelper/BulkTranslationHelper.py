"""
BulkTranslationHelper
"""

# Imports
import os
import json
import pandas as pd

from .TranslationOperations import TMSBulk_Clean_TMSJSON
from .TranslationOperations import TMSBulk_Join_TMSJSON
from .TranslationOperations import TMSBulk_Split_TMSJSON
from .TranslationOperations import TMSBulk_Convert_CSV_to_JSON
from .TranslationOperations import TMSBulk_Convert_CSV_to_Properties
from .TranslationOperations import TMSBulk_Convert_CSV_to_XLSX
from .TranslationOperations import TMSBulk_Convert_JSON_to_CSV
from .TranslationOperations import TMSBulk_Convert_JSON_to_YML
from .TranslationOperations import TMSBulk_Convert_Properties_to_CSV
from .TranslationOperations import TMSBulk_Convert_YML_to_JSON

from .TranslationOperations import TMSBulk_CombinedOperations

# Main Vars
OPERATIONS = {
    "Clean": {
        "tms_json": {
            "module": TMSBulk_Clean_TMSJSON,
            "input": {
                "type": "json",
                "count_type": "single"
            },
            "output": {
                "type": "json",
                "count_type": "single"
            }
        }
    },
    # "Join": {
    #     "tms_json": {
    #         "module": TMSBulk_Join_TMSJSON,
    #         "input": {
    #             "type": "json",
    #             "count_type": "multiple"
    #         },
    #         "output": {
    #             "type": "json",
    #             "count_type": "single"
    #         }
    #     }
    # },
    "Split": {
        "tms_json": {
            "module": TMSBulk_Split_TMSJSON,
            "input": {
                "type": "json",
                "count_type": "single"
            },
            "output": {
                "type": "json",
                "count_type": "multiple"
            }
        }
    },
    "Convert": {
        "csv_to_json": {
            "module": TMSBulk_Convert_CSV_to_JSON,
            "input": {
                "type": "csv",
                "count_type": "single"
            },
            "output": {
                "type": "json",
                "count_type": "single"
            }
        },
        "csv_to_properties": {
            "module": TMSBulk_Convert_CSV_to_Properties,
            "input": {
                "type": "csv",
                "count_type": "single"
            },
            "output": {
                "type": "properties",
                "count_type": "multiple"
            }
        },
        "csv_to_xlsx": {
            "module": TMSBulk_Convert_CSV_to_XLSX,
            "input": {
                "type": "csv",
                "count_type": "single"
            },
            "output": {
                "type": "xlsx",
                "count_type": "single"
            }
        },
        "json_to_csv": {
            "module": TMSBulk_Convert_JSON_to_CSV,
            "input": {
                "type": "json",
                "count_type": "single"
            },
            "output": {
                "type": "csv",
                "count_type": "single"
            }
        },
        "json_to_yml": {
            "module": TMSBulk_Convert_JSON_to_YML,
            "input": {
                "type": "json",
                "count_type": "single"
            },
            "output": {
                "type": "yml",
                "count_type": "single"
            }
        },
        "properties_to_csv": {
            "module": TMSBulk_Convert_Properties_to_CSV,
            "input": {
                "type": "properties",
                "count_type": "single"
            },
            "output": {
                "type": "csv",
                "count_type": "single"
            }
        },
        "yml_to_json": {
            "module": TMSBulk_Convert_YML_to_JSON,
            "input": {
                "type": "yml",
                "count_type": "single"
            },
            "output": {
                "type": "json",
                "count_type": "single"
            }
        }
    }
}

# Util Functions


# Main Functions


# Run Code