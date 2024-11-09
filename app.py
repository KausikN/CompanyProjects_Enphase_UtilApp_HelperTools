"""
Streamlit GUI for Helper Tools
"""

# Imports
import streamlit as st
from HelperTools import TOOL_APPS

# Main Vars


# App Functions
def app_main():
    '''
    App - Main
    '''
    # Title
    # st.markdown("# Workflow Helper")
    # Workflow
    USERINPUT_Workflow = st.sidebar.selectbox(
        "Select Tool",
        list(TOOL_APPS.keys())
    )
    TOOL_APPS[USERINPUT_Workflow]["func"]()

# Run Code
if __name__ == "__main__":
    # Assign Objects

    # Run App
    app_main()