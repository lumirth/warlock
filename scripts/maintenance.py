from pickler import *
from download_gpa import *
import os
import json

# Directory of pickles for GEN_EDS, GEN_ED_CODES, valid years, and valid subjects.
PICKLE_DIR = 'backend/api/pickles'
GPA_DATA_DIR = 'backend/api/data'
SHA_FILE = GPA_DATA_DIR + '/' + 'commit_sha.txt'
CSV_FILE = GPA_DATA_DIR + '/' +  'gpa.csv'
FEATHER_FILE = GPA_DATA_DIR + '/' + 'gpa.feather'

# DATA:
# - truth.json. A source of truth for GEN_EDS and GEN_ED_CODES. GEN_ED_CODES match banner exactly. GEN_EDS match reasonable expectation of gen ed name.
# - manual.json. Since GEN_EDS and subjects are fuzzy matched in the query parser, we add some manual correlations so that matching works as the user expects. For example, "comp sci" matching to "CS".
# - display.json. The display names for GEN_EDS and subjects. These are used in the UI. GEN_EDS match courses.illinois.edu/search/form exactly.
# the above may need to be refactored to be more intuitive, but for now, this works.
with open('scripts/data/truth.json', 'r') as f:
    dict_truth = json.load(f)    
with open('scripts/data/manual.json', 'r') as f:
    dict_manual = json.load(f)
with open('scripts/data/display.json', 'r') as f:
    dict_display = json.load(f)
    
GEN_EDS = {**dict_truth["GEN_EDS"], **dict_manual["MANUAL_GEN_EDS"], **dict_display["DISPLAY_GEN_EDS"]}
GEN_ED_CODES = {**dict_truth["GEN_ED_CODES"], **dict_manual["MANUAL_GEN_ED_CODES"], **dict_display["DISPLAY_GEN_ED_CODES"]}
MANUAL_SUBJECTS = dict_manual["MANUAL_SUBJECTS"]

# Access dictionaries from the loaded JSON data

# This is a maintenance script that does the following:
#   - Create pickles for data that isn't redefined often but CAN change (gen ed codes, valid years/subjects)
#       - Fetch the list of valid years from the UIUC course catalog.
#       - Using the valid years, fetch the list of valid subjects from the UIUC course catalog.
#       - Using the valid years, create a dictionary of valid terms for each year.
#       - Along with the defined GEN_EDS and GEN_ED_CODES, create a dictionary of data.
#       - Pickle the data into the PICKLE_DIR directory. (and verify it pickled correctly)
#   - Download the latest GPA data from Wade's datasets, if it hasn't already been downloaded.
#       - NOTE: If deleting the data, remember to delete commit_sha.txt as well.
if __name__ == '__main__':    
    print('Fetching data from UIUC course catalog...')
    years = fetch_years()
    subjects = fetch_subjects(years)
    subjects = {**subjects, **MANUAL_SUBJECTS}
    terms = fetch_terms(years)
    print('Successfully fetched data from UIUC course catalog.')
    for key, value in subjects.items():
        if (key != value):
            print(key, value)
    
    data = {
        'gen_eds': GEN_EDS,
        'gen_ed_codes': GEN_ED_CODES,
        'years': years,
        'subjects': subjects,
        'terms': terms,
    }
    print()
    print('Pickling data...')
    pickle_data_in_dir(data, PICKLE_DIR)
    print('Successfully pickled data.')
    
    print()
    print('Testing unpickling...')
    unpickled_gen_eds = unpickle_data(PICKLE_DIR + '/gen_eds.pkl')
    assert(unpickled_gen_eds == GEN_EDS)
    print('Successfully unpickled gen_eds.pkl.')
    
    print()
    print('Getting latest GPA data...')
    print('Checking hash of local CSV file...')
    previous_sha = get_previous_sha(SHA_FILE)
    print('Checking hash of latest CSV file...')
    latest_sha, download_url = get_latest_file_info()
    print('Checking whether the latest CSV file has already been downloaded and converted...')
    if latest_sha != previous_sha:
        download_and_convert_csv(download_url, CSV_FILE, FEATHER_FILE, SHA_FILE, latest_sha)
    else:
        print('The latest version of the CSV file has already been downloaded and converted.')
    print('Feather file should be located at: ' + FEATHER_FILE)