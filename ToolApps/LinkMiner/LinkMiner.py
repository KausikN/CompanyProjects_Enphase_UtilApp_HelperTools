"""
LinkMiner - Collect all links and similar text from a large text
"""

# Imports
import os
import re
from tqdm import tqdm

# Main Vars
PATHS = {
    "input_file": "Data/LinkMiner/Data/input.txt",
    "output_file": "Data/LinkMiner/Outputs/links.txt"
}
LINK_DATA = {
    # Links should start with any of these only (Eg. "http://haha.org" is accepted while "httpp://haha.org" is discarded)
    "link_identifiers": ["http://", "https://"],
    # Links should be separated from the rest of the text by any of these only (same separator should be used in start and end)
    "link_separators": ["'", '"', "`"],
}

# Main Functions
## Utils Functions
def Utils_ReadFile(path):
    '''
    Utils - Read a text file
    '''
    return str(open(path, "r").read())

def Utils_WriteLinks(links, path):
    '''
    Utils - Write links to a text file
    '''
    open(path, "w").write("\n".join(links))

## Link Mine Functions
def LinkMiner_ProcessLinkData(LINK_DATA):
    '''
    LinkMiner - Process Link Data to form useful metadata for link separation
    '''
    # Init
    PROCESSED_LINK_DATA = {}
    # Length Metadata
    for k in ["link_separators"]:
        link_data = LINK_DATA[k]
        link_data_lens = [len(ld) for ld in link_data]
        PROCESSED_LINK_DATA[k] = {
            "min_length": min(link_data_lens),
            "max_length": max(link_data_lens)
        }
    
    return PROCESSED_LINK_DATA


def LinkMiner_SeparateLinksFromText(TEXT, tqdm_disable=False, verbose=True):
    '''
    LinkMiner - Separate links from a large text
    '''
    # Init
    PROCESSED_LINK_DATA = LinkMiner_ProcessLinkData(LINK_DATA)

    # Separate text into lines (assuming a link can be only in one line)
    LINES = TEXT.split("\n")
    if verbose: print("LINES: ", len(LINES))

    # Get all occurences of link_identifiers in the text
    if verbose: print("\nCollecting all link occurences...")
    LINK_OCCURENCES = {link_identifier: [] for link_identifier in LINK_DATA["link_identifiers"]}
    for i in tqdm(range(len(LINES)), disable=tqdm_disable):
        if LINES[i].strip() == "": continue
        for link_identifier in tqdm(LINK_DATA["link_identifiers"], disable=True):
            CUR_LINE = LINES[i]
            while link_identifier in CUR_LINE:
                found_index = CUR_LINE.index(link_identifier)
                remaining_line = CUR_LINE[found_index+len(link_identifier):]
                ## Check if link separator is valid
                cur_line_updated = False
                if found_index >= PROCESSED_LINK_DATA["link_separators"]["min_length"]:
                    for link_separator in LINK_DATA["link_separators"]:
                        if (found_index >= len(link_separator)) and (CUR_LINE[found_index-len(link_separator):found_index] == link_separator):
                            ### Check if same link separator is in remaining line
                            if link_separator in remaining_line:
                                #### Link is from found_index to end_separator_found_index
                                end_separator_found_index = found_index+len(link_identifier) + remaining_line.index(link_separator)
                                LINK = CUR_LINE[found_index:end_separator_found_index]
                                LINK_OCCURENCES[link_identifier].append(LINK)
                                CUR_LINE = CUR_LINE[end_separator_found_index+1:]
                                cur_line_updated = True   
                                break
                if not cur_line_updated: CUR_LINE = remaining_line

    # Remove Direct Duplicates
    LINK_OCCURENCES_UNIQUE = {}
    if verbose: print("\nRemoving direct duplicates...")
    for link_identifier in tqdm(LINK_DATA["link_identifiers"], disable=tqdm_disable):
        LINK_OCCURENCES_UNIQUE[link_identifier] = list(set(LINK_OCCURENCES[link_identifier]))
    TOTAL_LINKS = sum([len(LINK_OCCURENCES[link_identifier]) for link_identifier in LINK_DATA["link_identifiers"]])
    TOTAL_LINKS_UNIQUE = sum([len(LINK_OCCURENCES_UNIQUE[link_identifier]) for link_identifier in LINK_DATA["link_identifiers"]])
    TOTAL_LINKS_DUPLICATE = TOTAL_LINKS - TOTAL_LINKS_UNIQUE
    if verbose: print("Total Links:", TOTAL_LINKS)
    if verbose: print("Unique Links:", TOTAL_LINKS_UNIQUE)
    if verbose: print("Duplicate Links:", TOTAL_LINKS_DUPLICATE)
    if verbose: print("\n")
    LINK_OCCURENCES = LINK_OCCURENCES_UNIQUE

    # Form Link List from Link Occurrences
    LINKS = []
    for k in LINK_OCCURENCES.keys(): LINKS.extend(LINK_OCCURENCES[k])
    LINKS = sorted(LINKS)
    if verbose: print("LINKS: ", len(LINKS))

    return LINKS

# Run Code

# ## Read Input File
# TEXT = Utils_ReadFile(PATHS["input_file"])

# ## Mine Links
# ### Separate links from all text
# LINKS = LinkMiner_SeparateLinksFromText(TEXT)

# ## Write Output File
# Utils_WriteLinks(LINKS, PATHS["output_file"])