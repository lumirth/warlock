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

# Load data from JSON file
with open('scripts/data.json', 'r') as f:
    data = json.load(f)

# Access dictionaries from the loaded JSON data
GEN_EDS = data['GEN_EDS']
GEN_EDS_MANUAL = data['GEN_EDS_MANUAL']
GEN_ED_CODES = data['GEN_ED_CODES']
MANUAL_SUBJECTS = data['MANUAL_SUBJECTS']

def add_manual_subjects(subj_dict):
    for key, value in MANUAL_SUBJECTS.items():
        subj_dict[key] = value

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
    add_manual_subjects(subjects)
    terms = fetch_terms(years)
    print('Successfully fetched data from UIUC course catalog.')
    for key, value in subjects.items():
        if (key != value):
            print(key, value)
    
    gen_eds = {**GEN_EDS, **GEN_EDS_MANUAL}
    data = {
        'gen_eds': gen_eds,
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
    assert(unpickled_gen_eds == gen_eds)
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