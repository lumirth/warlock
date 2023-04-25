import asyncio
import aiohttp
import xml.etree.ElementTree as ET

URL_FORM = "https://courses.illinois.edu/cisapp/explorer/schedule/{year}/{semester}.xml"
YEARS_URL = "https://courses.illinois.edu/cisapp/explorer/schedule.xml"

async def fetch_years():
    async with aiohttp.ClientSession() as session:
        async with session.get(YEARS_URL) as response:
            root = ET.fromstring(await response.content.read())
            years = set()
            for year in root.find("calendarYears"):
                years.add(year.attrib["id"])
            return years

async def fetch_subjects_worker(year, semester, print_prefix=''):
    url = URL_FORM.format(year=year, semester=semester)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            subjects = {}
            if response.status == 200:
                root = ET.fromstring(await response.content.read())
                for subject in root.find("subjects"):
                    subject_id = subject.attrib["id"]
                    subject_name = subject.text
                    subjects[subject_name] = subject_id
            return subjects

async def fetch_subjects(years, print_progress=False, print_prefix=''):
    default_year = max(map(int, years))
    tasks = []
    subjects = {}
    async with aiohttp.ClientSession() as session:
        for year in range(default_year, 2003, -1):
            for semester in ["fall", "spring", "summer", "winter"]:
                tasks.append(asyncio.create_task(fetch_subjects_worker(year, semester, print_prefix)))
        for future in asyncio.as_completed(tasks):
            subjects.update(await future)
    return subjects

async def fetch_terms_worker(year, print_prefix=''):
    url = 'https://courses.illinois.edu/cisapp/explorer/schedule/{year}.xml'.format(year=year)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            terms = set()
            if response.status == 200:
                root = ET.fromstring(await response.content.read())
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

async def fetch_terms(years, print_progress=False, print_prefix=''):
    terms = {}
    tasks = []
    async with aiohttp.ClientSession() as session:
        for year in years:
            tasks.append(asyncio.create_task(fetch_terms_worker(year, print_prefix)))
        for future in asyncio.as_completed(tasks):
            year, term_set = await future
            terms[year] = term_set
    return terms
