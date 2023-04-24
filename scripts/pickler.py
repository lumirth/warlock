import pickle
import requests
import os
import xml.etree.ElementTree as ET
import pprint

URL_FORM = "https://courses.illinois.edu/cisapp/explorer/schedule/{year}/{semester}.xml"
YEARS_URL = "https://courses.illinois.edu/cisapp/explorer/schedule.xml"

def fetch_years():
    req = requests.get(YEARS_URL)
    root = ET.fromstring(req.content)
    years = set()
    for year in root.find("calendarYears"):
        years.add(year.attrib["id"])
    return years


def fetch_subjects(years, print_progress=False, print_prefix=''):
    subjects = {}
    default_year = max(map(int, years))
    for year in range(default_year, 2003, -1):
        for semester in ["fall", "spring", "summer", "winter"]:
            url = URL_FORM.format(year=year, semester=semester)
            print("{}Fetching subjects from {}".format(print_prefix, url)) if print_progress else None
            response = requests.get(url)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                for subject in root.find("subjects"):
                    subject_id = subject.attrib["id"]
                    subject_name = subject.text
                    subjects[subject_name] = subject_id
                    subjects[subject_id] = subject_id
    return subjects

def fetch_terms(years, print_progress=False, print_prefix=''):
    # For each year, fetch the terms. Create a dictionary with the year as the key and a set of valid terms for that year as the value
    terms = {}
    for year in years:
        url = 'https://courses.illinois.edu/cisapp/explorer/schedule/{year}.xml'.format(year=year)
        print("{}Fetching terms from {}".format(print_prefix, url)) if print_progress else None
        response = requests.get(url)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            terms[year] = set()
            for term in root.find("terms"):
                if 'fall' in term.text.lower():
                    terms[year].add('fall')
                elif 'spring' in term.text.lower():
                    terms[year].add('spring')
                elif 'summer' in term.text.lower():
                    terms[year].add('summer')
                elif 'winter' in term.text.lower():
                    terms[year].add('winter')
    return terms

def pickle_data(data, file_path):
    with open(file_path, "wb") as file:
        pickle.dump(data, file)


def unpickle_data(file_path):
    with open(file_path, "rb") as file:
        return pickle.load(file)
    
def pretty_print(data, items_per_line=1, indent=0, spacing=1, space=' '):
    data_list = sorted(list(data))
    max_width = max(len(str(item)) for item in data_list)
    chunks = [data_list[i:i + items_per_line] for i in range(0, len(data_list), items_per_line)]
    table = ''
    for chunk in chunks:
        formatted_chunk = [f"{item:<{max_width}}" for item in chunk]
        table += (' ' * indent) + (space * spacing).join(formatted_chunk) + '\n'
    print(table)

# given a dictionary of dictionaries, with the keys being the directory names and the values being the data to be pickled
# pickles the data in the given directory
def pickle_data_in_dir(data, dir_name, print_progress=False):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    for file_name, data in data.items():
        if not file_name.endswith(".pkl"):
            file_name += ".pkl"
        pickle_data(data, os.path.join(dir_name, file_name))