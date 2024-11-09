"""
Streamlit GUI for Link Miner
"""

# Imports
import io
import streamlit as st
from .LinkMiner import *

# Main Vars

# Main Functions
def UI_LoadInputText():
    '''
    UI - Load Input Text
    '''
    # Init
    USERINPUT_Input = ""
    InputTypes = ["Text", "File"]
    # Load Input Type
    USERINPUT_InputType = st.selectbox("Input Type", InputTypes)
    # Load Input
    if USERINPUT_InputType == "File":
        USERINPUT_File = st.file_uploader("Input File")
        if USERINPUT_File is not None:
            USERINPUT_Input = str(io.StringIO(USERINPUT_File.getvalue().decode("utf-8")).read())
    else:
        USERINPUT_Input = st.text_area("Input Text")

    return USERINPUT_Input

# UI Functions
def UI_LinkMineVSCodeSearchText():
    '''
    UI - Mine Links from VS Code Search Text
    '''
    # Title
    st.markdown("# Link Miner - VS Code Search Text")

    # Load Prereq Inputs

    # Load Inputs
    USERINPUT_Input = UI_LoadInputText()

    # Process Inputs
    LINKS = LinkMiner_SeparateLinksFromText(USERINPUT_Input, tqdm_disable=True, verbose=False)

    # Display Outputs
    st.markdown("## Links")
    st.json(LINKS)


# UI Vars
TOOLS = {
    "Link Miner - VSCode Search": UI_LinkMineVSCodeSearchText
}

# App Functions
def app_main():
    '''
    App - Main
    '''
    # Title
    # st.markdown("# Link Miner")
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