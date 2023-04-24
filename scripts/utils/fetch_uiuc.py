import requests
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed

URL_FORM = "https://courses.illinois.edu/cisapp/explorer/schedule/{year}/{semester}.xml"
YEARS_URL = "https://courses.illinois.edu/cisapp/explorer/schedule.xml"

def fetch_years():
    req = requests.get(YEARS_URL)
    root = ET.fromstring(req.content)
    years = set()
    for year in root.find("calendarYears"):
        years.add(year.attrib["id"])
    return years

def fetch_subjects_worker(year, semester, print_prefix=''):
    url = URL_FORM.format(year=year, semester=semester)
    response = requests.get(url)
    subjects = {}
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        for subject in root.find("subjects"):
            subject_id = subject.attrib["id"]
            subject_name = subject.text
            subjects[subject_name] = subject_id
            subjects[subject_id] = subject_id
    return subjects

def fetch_subjects(years, print_progress=False, print_prefix='', max_workers=10):
    default_year = max(map(int, years))
    tasks = []
    subjects = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for year in range(default_year, 2003, -1):
            for semester in ["fall", "spring", "summer", "winter"]:
                tasks.append(executor.submit(fetch_subjects_worker, year, semester, print_prefix))
        for future in as_completed(tasks):
            subjects.update(future.result())
    return subjects

def fetch_terms_worker(year, print_prefix=''):
    url = 'https://courses.illinois.edu/cisapp/explorer/schedule/{year}.xml'.format(year=year)
    response = requests.get(url)
    terms = set()
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        for term in root.find("terms"):
            if 'fall' in term.text.lower():
                terms.add('fall')
            elif 'spring' in term.text.lower():
                terms.add('spring')
            elif 'summer' in term.text.lower():
                terms.add('summer')
            elif 'winter' in term.text.lower():
                terms.add('winter')
    return year, terms

def fetch_terms(years, print_progress=False, print_prefix='', max_workers=10):
    terms = {}
    tasks = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for year in years:
            tasks.append(executor.submit(fetch_terms_worker, year, print_prefix))
        for future in as_completed(tasks):
            year, term_set = future.result()
            terms[year] = term_set
    return terms