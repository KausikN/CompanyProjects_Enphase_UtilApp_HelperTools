"""
Streamlit GUI for Bulk Translation Helper
"""

# Imports
import yaml
import json
import shutil
import streamlit as st
from code_editor import code_editor
from .BulkTranslationHelper import *

import pandas as pd

# Main Vars
PATHS = {
    "save_params": {
        "input": {
            "dir": "Data/BulkTranslationHelper/Data/Temp/input/",
            "single": {
                "dir": "Data/BulkTranslationHelper/Data/Temp/input/",
                "name": "input"
            },
            "multiple": {
                "dir": "Data/BulkTranslationHelper/Data/Temp/input/",
                "prefix": "input_"
            }
        },
        "output": {
            "dir": "Data/BulkTranslationHelper/Data/Temp/output/",
            "single": {
                "dir": "Data/BulkTranslationHelper/Data/Temp/output/",
                "name": "output"
            },
            "multiple": {
                "dir": "Data/BulkTranslationHelper/Data/Temp/output/",
                "prefix": "output_"
            }
        }
    }
}

# Utils Functions
def Utils_GeneratePathParams(COUNT_TYPE, PATHS_DATA, OPERATION_EXT):
    '''
    Utils - Generate Path Params
    '''
    MULTIPLE_FILES = not (COUNT_TYPE == "single")
    PATH_PARAMS = {}

    if MULTIPLE_FILES:
        PATH_PARAMS = dict(PATHS_DATA["multiple"])
    else:
        PATH_PARAMS = {
            "path": os.path.join(PATHS_DATA["single"]["dir"], f"{PATHS_DATA['single']['name']}.{OPERATION_EXT}")
        }

    return PATH_PARAMS

def Utils_ClearDir(DIR_PATH):
    '''
    Utils - Clear all files in dir
    '''
    # Check if the directory exists
    if os.path.exists(DIR_PATH):
        try:
            # Remove the directory and all of its contents
            shutil.rmtree(DIR_PATH)
            print(f"Removed all contents of: {DIR_PATH}")
        except Exception as e:
            print(f"Error removing {DIR_PATH}: {e}")
            return
    
    # Recreate the empty directory
    os.makedirs(DIR_PATH)
    print(f"Recreated directory: {DIR_PATH}")

def Utils_ClearPrefixedFilesInDir(DIR_PATH, ACCEPT_FILE_PREFIXES=[]):
    '''
    Utils - Clear all files with name following given prefix in dir
    '''
    for root, dirs, files in os.walk(DIR_PATH):
        for file in files:
            check = False
            for FILE_PREFIX in ACCEPT_FILE_PREFIXES:
                if file.startswith(FILE_PREFIX): check = True
            if check:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Removed: {file_path}")
                except Exception as e:
                    print(f"Error removing {file_path}: {e}")

# Main Functions


# UI Functions
def UI_Input(INPUT_PARAMS, SAVE_PARAMS):
    '''
    UI - Input
    '''
    INPUT_TYPE = INPUT_PARAMS["type"]
    COUNT_TYPE = INPUT_PARAMS["count_type"]
    MULTIPLE_FILE_INPUT = not (COUNT_TYPE == "single")

    FILES = st.file_uploader(
        f"Upload {INPUT_TYPE} {'file' if MULTIPLE_FILE_INPUT else 'files'}",
        type=[INPUT_TYPE],
        accept_multiple_files=MULTIPLE_FILE_INPUT
    )

    if MULTIPLE_FILE_INPUT:
        for i in range(len(FILES)):
            FILE = FILES[i]
            if FILE is not None:
                SAVE_PATH = os.path.join(SAVE_PARAMS["multiple"]["dir"], f"{SAVE_PARAMS['multiple']['prefix']}{i}.{INPUT_TYPE}")
                with open(SAVE_PATH, "wb") as f: f.write(FILE.getbuffer())
    else:
        FILE = FILES
        if FILE is not None:
            SAVE_PATH = os.path.join(SAVE_PARAMS["single"]["dir"], f"{SAVE_PARAMS['single']['name']}.{INPUT_TYPE}")
            with open(SAVE_PATH, "wb") as f: f.write(FILE.getbuffer())

def UI_RunOperation(OPERATION):
    '''
    UI - Run Operation
    '''
    MODULE = OPERATION["module"]
    INPUT_PARAMS = OPERATION["input"]
    OUTPUT_PARAMS = OPERATION["output"]
    OPERATION_FROM = MODULE.OPERATION_FROM
    OPERATION_TO = MODULE.OPERATION_TO

    PATH_PARAMS = {
        "input": Utils_GeneratePathParams(INPUT_PARAMS["count_type"], PATHS["save_params"]["input"], OPERATION_FROM),
        "output": Utils_GeneratePathParams(OUTPUT_PARAMS["count_type"], PATHS["save_params"]["output"], OPERATION_TO)
    }

    MODULE.PATHS.update(PATH_PARAMS)

    MODULE.run()

def UI_DisplayAllOutputFiles(DIR_PATH, IGNORE_FILE_PREFIXES=[]):
    '''
    UI - Display all files in output dir in UI
    '''
    if not os.path.exists(DIR_PATH):
        st.error(f"Output directory does not exist.")
        return
    
    FILES = sorted(os.listdir(DIR_PATH))
    if not FILES:
        st.info("No Output files generated.")
        return
    
    for FILE in FILES:
        skip = False
        for FILE_PREFIX in IGNORE_FILE_PREFIXES:
            if FILE.startswith(FILE_PREFIX): skip = True
        if skip: continue
        file_path = os.path.join(DIR_PATH, FILE)
        size_kb = os.path.getsize(file_path) / 1024

        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"📄 **{FILE}** — `{size_kb:.1f} KB`")
        with col2:
            with open(file_path, "rb") as f:
                st.download_button(
                    label="⬇️",
                    data=f,
                    file_name=FILE,
                    mime="application/octet-stream",
                    use_container_width=True
                )

def UI_CommonProcess(OPERATION):
    '''
    UI - Common Process
    '''
    MODULE = OPERATION["module"]
    INPUT_PARAMS = OPERATION["input"]
    OUTPUT_PARAMS = OPERATION["output"]

    UI_Input(INPUT_PARAMS, PATHS["save_params"]["input"])

    USERINPUT_Process = st.checkbox("Process")
    if not USERINPUT_Process: return

    Utils_ClearPrefixedFilesInDir(
        PATHS["save_params"]["output"]["dir"],
        [PATHS["save_params"]["output"]["multiple"]["prefix"], PATHS["save_params"]["output"]["single"]["name"]]
    )

    UI_RunOperation(OPERATION)

    st.subheader("📂 Output Files")
    UI_DisplayAllOutputFiles(
        PATHS["save_params"]["output"]["dir"],
        ["test"]
    )

# UI Vars


# App Functions
def app_main():
    '''
    App - Main
    '''
    # Title
    # st.markdown("# Bulk Translation Helper")
    # Operation Type
    USERINPUT_OperationType = st.sidebar.selectbox(
        "Select Operation Type",
        list(OPERATIONS.keys())
    )
    st.header(f"Translation Bulk Operation: {USERINPUT_OperationType}")
    # Operation
    USERINPUT_Operation = st.selectbox(
        "Select Operation",
        list(OPERATIONS[USERINPUT_OperationType].keys())
    )

    # Process
    UI_CommonProcess(OPERATIONS[USERINPUT_OperationType][USERINPUT_Operation])

# Run Code
if __name__ == "__main__":
    # Assign Objects

    # Run App
    app_main()