"""
Streamlit GUI for Translation Helper
"""

# Imports
import json
import streamlit as st
from code_editor import code_editor
from .TranslationHelper import *

import pandas as pd

# Main Vars

# Main Functions


# UI Functions
def UI_CSV_to_JSON():
    '''
    UI - CSV to JSON
    '''
    # Title
    st.markdown("# Translations CSV to JSON")

    # Load CSV File
    st.markdown("## Inputs")
    USERINPUT_File = st.file_uploader(
        "Upload CSV File", ["csv"], 
        accept_multiple_files=False
    )
    if USERINPUT_File is None: st.stop()
    ## Read CSV
    data = pd.read_csv(USERINPUT_File)
    st.write(data)
    TRANSLATIONS_DATA = {
        "languages": data.columns,
        "translations": data
    }

    # Format Data
    st.markdown("## JSON Template")
    JSON_TEMPLATE = json.loads(code_editor("{\n\n}", lang="json", response_mode="debounce")["text"])

    FORMATTED_TRANSATIONS = TranslationHelper_FormatTranslationsOnJSONTemplate(
        TRANSLATIONS_DATA["translations"],
        JSON_TEMPLATE
    )

    # Output
    st.markdown("## Outputs")
    for language in FORMATTED_TRANSATIONS.keys():
        st.markdown(f"#### Language: {language}")
        st.json(FORMATTED_TRANSATIONS[language], expanded=True)

def UI_JSON_to_CSV():
    '''
    UI - CSV to JSON
    '''
    pass

# UI Vars
TOOLS = {
    "CSV to JSON": UI_CSV_to_JSON,
    "JSON to CSV": UI_JSON_to_CSV
}

# App Functions
def app_main():
    '''
    App - Main
    '''
    # Title
    # st.markdown("# Translation Helper")
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