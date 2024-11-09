"""
Helper Tools
"""

# Imports
from ToolApps.LinkMiner import app as APP_ToolMiner
from ToolApps.SiteHelper import app as APP_SiteHelper
from ToolApps.TranslationHelper import app as APP_TranslationHelper

# Main Vars
TOOL_APPS = {
    "LinkMiner": {
        "module": APP_ToolMiner,
        "func": APP_ToolMiner.app_main
    },
    "SiteHelper": {
        "module": APP_SiteHelper,
        "func": APP_SiteHelper.app_main
    },
    "TranslationHelper": {
        "module": APP_TranslationHelper,
        "func": APP_TranslationHelper.app_main
    }
}