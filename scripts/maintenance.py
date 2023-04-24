from utils.pickler import *
from utils.download_gpa import *
from utils.fetch_uiuc import *
import json
import sys

# Command line argument for # max workers (default 10)
if len(sys.argv) > 1:
    MAX_WORKERS = int(sys.argv[1])
else:
    MAX_WORKERS = 10

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

def main():
    years = set()
    subjects = dict()
    terms = set()
    
    def _fetch_data_from_uiuc():
        print('Fetching data from UIUC course catalog...')
        years = fetch_years()
        subjects = fetch_subjects(years, max_workers=MAX_WORKERS)
        subjects = {**subjects, **MANUAL_SUBJECTS}
        terms = fetch_terms(years, max_workers=MAX_WORKERS)
        print('Successfully fetched data from UIUC course catalog.')
        
    def _pickle_data():
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
        
    def _test_unpickling():
        print()
        print('Testing unpickling...')
        unpickled_gen_eds = unpickle_data(PICKLE_DIR + '/gen_eds.pkl')
        assert(unpickled_gen_eds == GEN_EDS)
        print('Successfully unpickled gen_eds.pkl.')

    def _get_csv_data():
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
    
    _fetch_data_from_uiuc()
    _pickle_data()
    _test_unpickling()
    _get_csv_data()

if __name__ == '__main__':    
    main()