"""
TMS Bulk - Convert Formats

Sample CSV Structure:
| key                 | en        | fr        |
|---------------------|-----------|-----------|
| mobile.nav.str      | Hello     | Bonjour   |
| mobile.nav.array[0] | V1        | V2        |

Sample JSON Structure:
{
    "en": {
        "mobile": {
            "nav": {
                "str": "Hello",
                "array": ["V1"]
            }
        }
    },
    "fr": {
        "mobile": {
            "nav": {
                "str": "Bonjour",
                "array": ["V2"]
            }
        }
    }
}
"""

# Imports
import json
import pandas as pd
from tqdm import tqdm

# Utils Functions
def Utils_MergeDicts(a, b):
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                Utils_MergeDicts(a[key], b[key])
            elif isinstance(a[key], list) and isinstance(b[key], list):
                for i in range(len(b[key])):
                    if i < len(a[key]) and a[key][i] is not None and b[key][i] is not None:
                        if isinstance(a[key][i], dict) and isinstance(b[key][i], dict):
                            Utils_MergeDicts(a[key][i], b[key][i])
                        else:
                            a[key][i] = b[key][i]
                    elif i < len(a[key]):
                        continue
                    else:
                        a[key].append(b[key][i])
            else:
                a[key] = b[key]
        else:
            a[key] = b[key]

# Print Functions
def Print_CSVMetadata(CSV_DATA, header=""):
    print()
    print(f"{header}")
    print("Row Count: ", len(CSV_DATA))
    print(CSV_DATA.head())
    print()

# Main Functions
## Recursive Functions
def TMSBulk_Recursive_JointKeyList2Dict(current_key_parts, value):
    '''
    Recursive helper function to create nested dictionaries/lists based on key parts.
    '''
    if not current_key_parts:
        return value

    part = current_key_parts[0]

    # Check for array index notation (e.g., 'array[0]')
    if '[' in part and ']' in part:
        array_name, index_str = part.split('[')
        array_name = array_name.strip()
        index = int(index_str.strip(']'))

        # Create a list with None placeholders
        lst = []
        while len(lst) <= index: lst.append(None)

        # Recursively create the nested structure for the rest of the key parts
        lst[index] = TMSBulk_Recursive_JointKeyList2Dict(current_key_parts[1:], value)
        return {array_name: lst}
    else:
        # Regular dictionary key
        return {part: TMSBulk_Recursive_JointKeyList2Dict(current_key_parts[1:], value)}
    
def TMSBulk_Recursive_Dict2JointKeyList(current_obj, parent_key=None, value_key_name="value"):
    '''
    Recursive helper function to extract key-value pairs from nested dictionaries/lists.
    '''
    csv_data_list = []

    if isinstance(current_obj, dict):
        for key, value in current_obj.items():
            new_key = f"{parent_key}.{key}" if parent_key is not None else key
            items = TMSBulk_Recursive_Dict2JointKeyList(value, new_key, value_key_name)
            csv_data_list.extend(items)
    elif isinstance(current_obj, list):
        for index, item in enumerate(current_obj):
            new_key = f"{parent_key}[{index}]"
            items = TMSBulk_Recursive_Dict2JointKeyList(item, new_key, value_key_name)
            csv_data_list.extend(items)
    else:
        # Base case: reached a leaf node
        row = {'key': parent_key, value_key_name: current_obj}
        csv_data_list.append(row)

    return csv_data_list

## Convert Functions
def TMSBulk_Convert_CSV_to_JSON(CSV_DATA):
    '''
    TMS Bulk - Convert CSV data to JSON format
    '''
    # Identify language columns (all columns except 'key')
    lang_cols = [col for col in CSV_DATA.columns if col != 'key']
    
    # Initialize the output dictionary
    JSON_DATA = {lang: {} for lang in lang_cols}

    # Iterate over each row (localization entry)
    for lang in tqdm(lang_cols):
        for _, row in CSV_DATA.iterrows():
            key_path = row['key']
            value = row[lang]

            # Split the key path into parts
            key_parts = key_path.split('.')

            # Create the nested structure for this key-value pair
            nested_object = TMSBulk_Recursive_JointKeyList2Dict(key_parts, value)

            # Merge the nested object into the main JSON structure
            Utils_MergeDicts(JSON_DATA[lang], nested_object)

    return JSON_DATA

def TMSBulk_Convert_JSON_to_CSV(JSON_DATA):
    '''
    TMS Bulk - Convert JSON data to CSV format
    '''
    # Identify language columns (all columns except 'key')
    lang_cols = list(JSON_DATA.keys())
    
    # Initialize the output csv data list
    csv_data = []

    # Start recursive extraction for each language
    for lang in tqdm(lang_cols):
        lang_csv_data = TMSBulk_Recursive_Dict2JointKeyList(JSON_DATA[lang], parent_key=None)
        for row in lang_csv_data:
            # Find if this key already exists in csv_data
            existing_row = next((item for item in csv_data if item['key'] == row['key']), None)
            if existing_row:
                existing_row[lang] = row['value']
            else:
                new_row = {'key': row['key'], lang: row['value']}
                csv_data.append(new_row)

    # Convert list of rows to DataFrame
    CSV_DATA = pd.DataFrame(csv_data)

    return CSV_DATA

## Filter Functions
def TMSBulk_Filter_ArrayKeys(CSV_DATA, negative_filter=False):
    filtered_rows_list = []
    for _, row in CSV_DATA.iterrows():
        key_path = row['key']

        check = "[" in key_path and "]" in key_path

        if negative_filter: check = not check
        if check: filtered_rows_list.append(row.to_dict())
    FILTERED_ROWS = pd.DataFrame(filtered_rows_list)

    return FILTERED_ROWS

def TMSBulk_Filter_PrefixesFilter(CSV_DATA, prefixes=[], negative_filter=False):
    filtered_rows_list = []
    for _, row in CSV_DATA.iterrows():
        key_path = row['key']

        check = True in [key_path.startswith(p) for p in prefixes]

        if negative_filter: check = not check
        if check: filtered_rows_list.append(row.to_dict())
    FILTERED_ROWS = pd.DataFrame(filtered_rows_list)

    return FILTERED_ROWS

# Main Vars


# Run Code