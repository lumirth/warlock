from pickler import *
from download_gpa import *
import os

# change directory to the directory of this file
# this script creates a directory in the parent directory of the directory of this file
# meaning, if script is in folder/scripts, the directory created will be folder/data
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# GEN_EDS defines the mapping of a full gen ed name ot its Banner code.
GEN_EDS = {
    'Composition I': 'COMP1',
    'Advanced Composition': '1CLL',
    'Humanities and the Arts': 'HUM',
    'Literature & the Arts': '1LA',
    'Historical & Philosophical ': '1HP',
    'Natural Sciences and Technology': 'NAT',
    'Life Science': '1LS',
    'Physical Science': '1PS',
    'Quantitative Reasoning I': '1QR1',
    'Quantitative Reasoning II': '1QR2',
    'Social and Behavioral Sciences': 'SBS',
    'Social Science': '1SS',
    'Behavioral Science': '1BSC',
    'Cultural Studies': 'CS',
    'Western/Comparative Cultures': '1WCC',
    'Non-Western Cultures': '1NW',
    'US Minority Cultures': '1US',
}
# GEN_ED_CODES defines the mapping of a number of warlock-valid gen ed codes to their Banner code.
GEN_ED_CODES = {
    'COMP1': 'COMP1',
    '1CLL': '1CLL',
    'HUM': 'HUM',
    '1LA': '1LA',
    '1HP': '1HP',
    'NAT': 'NAT',
    '1LS': '1LS',
    '1PS': '1PS',
    '1QR1': '1QR1',
    '1QR2': '1QR2',
    'SBS': 'SBS',
    '1SS': '1SS',
    '1BSC': '1BSC',
    'CS': 'CS',
    '1WCC': '1WCC',
    '1NW': '1NW',
    '1US': '1US',
    'CP': 'COMP1',
    'ACP': '1CLL',
    'HUM': 'HUM',
    'HUM-LA': '1LA',
    'HUM-HP': '1HP',
    'NAT': 'NAT',
    'NAT-LS': '1LS',
    'NAT-PS': '1PS',
    'QR-I': '1QR1',
    'QR-I': '1QR2',
    'SBS': 'SBS',
    'SBS-SS': '1SS',
    'SBS-BS': '1BSC',
    'CS': 'CS',
    'CS-WCC': '1WCC',
    'CS-NW': '1NW',
    'CS-US': '1US',
    'COMP': 'COMP1',
    'ADVCOMP': '1CLL',
    'LITART': '1LA',
    'LIT': '1LA',
    'HISTPHIL': '1HP',
    'HIST': '1HP',
    'LIFE': '1LS',
    'PHYS': '1PS',
    'QR1': '1QR1',
    'QR2': '1QR2',
    'SOCBEH': 'SBS',
    'SOC': '1SS',
    'BEH': '1BSC',
    'CULT': 'CS',
    'WEST': '1WCC',
    'NWEST': '1NW',
    'NONWEST': '1NW',
    'MIN': '1US',
    'MINORITY': '1US',
}
# Directory of pickles for GEN_EDS, GEN_ED_CODES, valid years, and valid subjects.
PICKLE_DIR = '../pickles'
GPA_DATA_DIR = '../data'
SHA_FILE = GPA_DATA_DIR + '/' + 'commit_sha.txt'
CSV_FILE = GPA_DATA_DIR + '/' +  'gpa.csv'
FEATHER_FILE = GPA_DATA_DIR + '/' + 'gpa.feather'

# This is a bit of a bandaid to make fuzzy matching some common shorthand nicer
# We can add to this as needed to make fuzzy matching more accurate
MANUAL_SUBJECTS = {
    'comp sci': 'CS',
    'anthro': 'ANTH',
    'crop sci': 'CPSC',
    'classic civ': 'CLCV',
    'coms': 'COMM'
    
}

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