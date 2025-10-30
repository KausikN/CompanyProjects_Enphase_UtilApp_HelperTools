"""
Streamlit GUI for Bulk Translation Helper
"""

# Imports
import copy
import shutil
import streamlit as st
from stqdm import stqdm
from .BulkTranslationHelper import *

# Main Vars
PATHS = {
    "save_params": {
        "input": {
            "dir": "Data/BulkTranslationHelper/Data/Temp/input/",
            "single": {
                "name": "input"
            },
            "multiple": {
                "prefix": "input_"
            }
        },
        "output": {
            "dir": "Data/BulkTranslationHelper/Data/Temp/output/",
            "single": {
                "name": "output"
            },
            "multiple": {
                "prefix": "output_"
            }
        }
    }
}
USE_GENERIC_DIR_CLEARING = True

# Utils Functions
def Utils_GeneratePathParams(COUNT_TYPE, PATHS_DATA, OPERATION_EXT):
    '''
    Utils - Generate Path Params
    '''
    MULTIPLE_FILES = not (COUNT_TYPE == "single")
    PATH_PARAMS = {}

    if MULTIPLE_FILES:
        PATH_PARAMS = {
            "dir": PATHS_DATA["dir"],
            "prefix": PATHS_DATA["multiple"]["prefix"]
        }
    else:
        PATH_PARAMS = {
            "path": os.path.join(PATHS_DATA["dir"], f"{PATHS_DATA['single']['name']}.{OPERATION_EXT}")
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
def UI_Input(INPUT_PARAMS, SAVE_PARAMS, BULK_OPERATION=False):
    '''
    UI - Input
    '''
    INPUT_TYPE = INPUT_PARAMS["type"]
    COUNT_TYPE = INPUT_PARAMS["count_type"]
    MULTIPLE_FILE_INPUT = (not (COUNT_TYPE == "single")) or BULK_OPERATION

    FILE_NAMES = []

    FILES = st.file_uploader(
        f"Upload {INPUT_TYPE} {'files' if MULTIPLE_FILE_INPUT else 'file'}",
        type=[INPUT_TYPE],
        accept_multiple_files=MULTIPLE_FILE_INPUT
    )

    if MULTIPLE_FILE_INPUT:
        for i in range(len(FILES)):
            FILE = FILES[i]
            if FILE is not None:
                os.makedirs(SAVE_PARAMS["dir"], exist_ok=True)
                SAVE_PATH = os.path.join(SAVE_PARAMS["dir"], f"{SAVE_PARAMS['multiple']['prefix']}{i}.{INPUT_TYPE}")
                with open(SAVE_PATH, "wb") as f: f.write(FILE.getbuffer())
                FILE_NAMES.append(FILE.name)
    else:
        FILE = FILES
        if FILE is not None:
            os.makedirs(SAVE_PARAMS["dir"], exist_ok=True)
            SAVE_PATH = os.path.join(SAVE_PARAMS["dir"], f"{SAVE_PARAMS['single']['name']}.{INPUT_TYPE}")
            with open(SAVE_PATH, "wb") as f: f.write(FILE.getbuffer())
            FILE_NAMES.append(FILE.name)

    return FILE_NAMES

def UI_RunOperation(OPERATION, OPERATION_SAVE_PARAMS):
    '''
    UI - Run Operation
    '''
    MODULE = OPERATION["module"]
    INPUT_PARAMS = OPERATION["input"]
    OUTPUT_PARAMS = OPERATION["output"]
    OPERATION_FROM = MODULE.OPERATION_FROM
    OPERATION_TO = MODULE.OPERATION_TO

    os.makedirs(OPERATION_SAVE_PARAMS["output"]["dir"], exist_ok=True)

    PATH_PARAMS = {
        "input": Utils_GeneratePathParams(INPUT_PARAMS["count_type"], OPERATION_SAVE_PARAMS["input"], OPERATION_FROM),
        "output": Utils_GeneratePathParams(OUTPUT_PARAMS["count_type"], OPERATION_SAVE_PARAMS["output"], OPERATION_TO)
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

def UI_CommonProcess(OPERATION, OPERATION_KEY=""):
    '''
    UI - Common Process
    '''
    MODULE = OPERATION["module"]
    INPUT_PARAMS = OPERATION["input"]
    OUTPUT_PARAMS = OPERATION["output"]

    USERINPUT_BulkMode = False
    if OPERATION["input"]["count_type"] == "single":
        USERINPUT_BulkMode = st.sidebar.checkbox("Bulk Mode", key=f"BULK_MODE_CHECKBOX_{OPERATION_KEY}")

    FILE_NAMES = UI_Input(INPUT_PARAMS, PATHS["save_params"]["input"], BULK_OPERATION=USERINPUT_BulkMode)

    USERINPUT_Process = st.checkbox("Process", key=f"PROCESS_CHECKBOX_{OPERATION_KEY}")
    if len(FILE_NAMES) == 0 or not USERINPUT_Process: return

    if USE_GENERIC_DIR_CLEARING:
        Utils_ClearDir(PATHS["save_params"]["output"]["dir"])
    else:
        Utils_ClearPrefixedFilesInDir(
            PATHS["save_params"]["output"]["dir"],
            [PATHS["save_params"]["output"]["multiple"]["prefix"], PATHS["save_params"]["output"]["single"]["name"]]
        )

    if USERINPUT_BulkMode:
        for i in stqdm(range(len(FILE_NAMES)), desc="Processing Files"):
            CUR_FILE_NAME_NOEXT = os.path.splitext(FILE_NAMES[i])[0]
            CUR_SAVE_PARAMS = copy.deepcopy(PATHS["save_params"])
            CUR_SAVE_PARAMS["input"]["single"]["name"] = f"{PATHS['save_params']['input']['multiple']['prefix']}{i}"
            CUR_SAVE_PARAMS["output"]["single"]["name"] = CUR_FILE_NAME_NOEXT
            CUR_SAVE_PARAMS["output"]["multiple"]["prefix"] = f"{CUR_FILE_NAME_NOEXT}_"
            UI_RunOperation(OPERATION, CUR_SAVE_PARAMS)
    else:
        CUR_FILE_NAME_NOEXT = os.path.splitext(FILE_NAMES[0])[0]
        CUR_SAVE_PARAMS = copy.deepcopy(PATHS["save_params"])
        if INPUT_PARAMS["count_type"] == "single":
            CUR_SAVE_PARAMS["output"]["single"]["name"] = CUR_FILE_NAME_NOEXT
            CUR_SAVE_PARAMS["output"]["multiple"]["prefix"] = f"{CUR_FILE_NAME_NOEXT}_"
        UI_RunOperation(OPERATION, CUR_SAVE_PARAMS)

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
    UI_CommonProcess(OPERATIONS[USERINPUT_OperationType][USERINPUT_Operation], f"{USERINPUT_OperationType}_{USERINPUT_Operation}")

# Run Code
if __name__ == "__main__":
    # Assign Objects

    # Run App
    app_main()