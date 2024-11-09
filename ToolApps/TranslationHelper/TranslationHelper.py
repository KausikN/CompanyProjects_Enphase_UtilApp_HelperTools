"""
SiteHelper
"""

# Imports
import os
import json
import pandas as pd

# Main Vars


# Util Functions
def JSONTemplate_RecursiveFunc(template, replacements):
    '''
    JSON Template - Recursive Function
    '''
    for k in template.keys():
        k_type = type(template[k])
        if k_type in [str]: continue
        if k_type in [dict]: template[k] = JSONTemplate_RecursiveFunc(template[k], replacements)
        elif k_type in [int]: template[k] = replacements[template[k]-1]

    return template

# Main Functions
def TranslationHelper_FormatTranslationsOnJSONTemplate(translations, template):
    '''
    Translation Helper - Format Translations on JSON Template
    '''
    # Init
    FORMATTED_TRANSLATIONS = {}
    languages = translations.columns
    # Format
    for langauge in languages:
        FORMATTED_TRANSLATIONS[langauge] = json.loads(json.dumps(template, indent=4))
        FORMATTED_TRANSLATIONS[langauge] = JSONTemplate_RecursiveFunc(FORMATTED_TRANSLATIONS[langauge], translations[langauge])

    return FORMATTED_TRANSLATIONS

# Run Code