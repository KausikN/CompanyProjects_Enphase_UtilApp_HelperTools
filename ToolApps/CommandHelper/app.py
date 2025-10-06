"""
Streamlit GUI for Commands and Scripts Helper
"""

# Imports
import uuid
import json
import streamlit as st
from code_editor import code_editor
from .CommandHelper import *

# Utils Functions
def Utils_GenerateFieldKey_RandomUID():
    '''
    Utils - Generate UID Randomly
    '''
    return str(uuid.uuid4())

def Utils_GenerateFieldKey_InputBasedUID(inp=""):
    '''
    Utils - Generate UID based on Input
    '''
    return str(uuid.uuid5(uuid.NAMESPACE_OID, inp))


# Main Vars

# Main Functions
def UI_GetParams(PARAMS_DATA, key_prefix=""):
    '''
    UI - Get Params
    '''
    # Init
    USERINPUT_Params = {}
    # Load Params
    for k in PARAMS_DATA.keys():
        p = PARAMS_DATA[k]
        uid_key = key_prefix + "_" + k
        if p["type"] == "selection":
            USERINPUT_Params[k] = st.selectbox(p["name"], **p["params"], key=Utils_GenerateFieldKey_InputBasedUID(uid_key))
        elif p["type"] == "number":
            USERINPUT_Params[k] = p["datatype"](st.number_input(p["name"], **p["params"], key=Utils_GenerateFieldKey_InputBasedUID(uid_key)))
        elif p["type"] == "json":
            USERINPUT_Params[k] = json.loads(st.text_area(p["name"], **p["params"], key=Utils_GenerateFieldKey_InputBasedUID(uid_key)))
        elif p["type"] == "text":
            USERINPUT_Params[k] = st.text_input(p["name"], **p["params"], key=Utils_GenerateFieldKey_InputBasedUID(uid_key))
        elif p["type"] == "code_editor":
            USERINPUT_Params[k] = code_editor(**p["params"])
        elif p["type"] == "constant":
            st.text_input(p["name"], value=str(p["value"]), disabled=True, key=Utils_GenerateFieldKey_InputBasedUID(uid_key))
            USERINPUT_Params[k] = p["value"]
        else:
            USERINPUT_Params[k] = None

    return USERINPUT_Params

def UI_GetCommandOutput(COMMAND, INPUTS={}):
    '''
    UI - Get Outputs
    '''
    # Init
    OUTPUTS = {}
    OUTPUT_DATA = COMMAND["output"]

    # Form Outputs
    OUT = None
    if OUTPUT_DATA["compute"] == "func":
        OUT = OUTPUT_DATA["func"](**INPUTS)
    else:
        OUT = OUTPUT_DATA["value"].format(**INPUTS)

    # Display Outputs
    if OUTPUT_DATA["type"] == "text":
        st.markdown(f"```\n{OUT}\n```")
    elif OUTPUT_DATA["type"] == "code":
        st.code(OUT, **OUTPUT_DATA["params"])

# UI Functions
def UI_Commands():
    '''
    UI - Commands
    '''
    # Title
    st.title("Commands")

    # Load Prereq Inputs
    

    # Load Inputs, Display Outputs
    for k in COMMANDS_DATA:
        with st.expander(k, expanded=False):
            COMMON_DATA = COMMANDS_DATA[k]["common"]
            COMMANDS = COMMANDS_DATA[k]["commands"]
            USERINPUT_CommonParams = UI_GetParams(COMMON_DATA["inputs"], key_prefix=k)
            for i in range(len(COMMANDS)):
                command = COMMANDS[i]
                st.subheader(command["name"])
                USERINPUT_Params = UI_GetParams(command["inputs"], key_prefix=command["name"])
                USERINPUT_Params = {**USERINPUT_CommonParams, **USERINPUT_Params}
                UI_GetCommandOutput(command, USERINPUT_Params)

# UI Vars
TOOLS = {
    "Commands": UI_Commands
}

# App Functions
def app_main():
    '''
    App - Main
    '''
    # Title
    # st.markdown("# Command Helper")
    # Tool
    USERINPUT_Tool = st.sidebar.selectbox(
        "Select Tool",
        list(TOOLS.keys())
    )
    TOOLS[USERINPUT_Tool]()

# Run Code
if __name__ == "__main__":
    # Assign Objects

    # Run App
    app_main()