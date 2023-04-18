from typing import Optional
from models import AdvancedSearchParameters
import time
import re
import pickle
from fuzzywuzzy import fuzz, process
import os

DEBUG = True
DEFAULT_YEAR = time.localtime().tm_year
DEFAULT_SEMESTER = 'fall' if time.localtime().tm_mon > 3 else 'spring'

FUZZ_THRESH = 70

# change directory to the directory of this file
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# unpickle unchanging data
PICKLES_DIR = './pickles'
GEN_EDS = pickle.load(open(os.path.join(PICKLES_DIR, 'gen_eds.pkl'), 'rb'))
GEN_ED_CODES = pickle.load(open(os.path.join(PICKLES_DIR, 'gen_ed_codes.pkl'), 'rb'))
YEARS = pickle.load(open(os.path.join(PICKLES_DIR, 'years.pkl'), 'rb'))
SUBJECTS = pickle.load(open(os.path.join(PICKLES_DIR, 'subjects.pkl'), 'rb'))
TERMS = pickle.load(open(os.path.join(PICKLES_DIR, 'terms.pkl'), 'rb'))

COLON_ARGS = {
    'year': ('year', 'yr', 'y'),
    'semester': ('semester', 'sem', 'term', 's', 't'),
    'pot': ('pot'),
    'subject': ('subj', 'subject', 'dept', 'department', 'd'),
    'course_id': ('id', 'course id', 'courseid', 'course-id', 'number', 'num', 'n'),
    'course': ('course', 'crs', 'c'),
    'crn': ('crn', 'r'),
    'hours': ('hrs', 'hr', 'hours', 'hour', 'h'),
    'instructor': ('prof', 'professor', 'instructor', 'inst', 'p'),
    'gen_ed': ('gened', 'gen-ed', 'gen ed', 'ge', 'g'),
    'is': ('is')
}
IS_ARGS = {
    'online': ('online', 'on', 'o'),
    'campus': ('campus', 'on-campus', 'on campus', 'oncampus', 'c'),
    'open': ('open', 'o')
}
SEMESTER = {
    'fa': 'fall',
    'sp': 'spring',
    'su': 'summer',
    'wi': 'winter',
    'fall': 'fall',
    'spring': 'spring',
    'summer': 'summer',
    'winter': 'winter',
    'fal': 'fall',
    'spr': 'spring',
    'sum': 'summer',
    'win': 'winter',
}

class AdvancedQueryStringParser:
    def __init__(self, input_string: str):
        self.input_string = input_string
        self.advanced_query = AdvancedSearchParameters()

    def parse(self) -> AdvancedSearchParameters:
        # Implement parsing logic to convert input_string into an AdvancedSearchParameters object
        tokens = self.input_string.split(',')

        for token in tokens:
            self._parse_token(token)

        return self.advanced_query

    def _parse_token(self, token):
        if len(token) > 7:
            print('match fuzzy')
            if self._match_gen_ed_fuzzy(token):
                return
        if not ':' in token and len(token) <= 8:
            print('match subj and id')
            if self._match_subj_and_id_regex(token):
                return
        if token.isdigit() and len(token) == 5:
            print('match crn')
            self.advanced_query.crn = token
            return
        if ':' in token:
            print('match colon args')
            self._match_colon_args(token)
            return
        print('match keyword')
        self.advanced_query.keyword = token

    def _match_gen_ed_fuzzy(self, token):
        print('token: ', token)
        gen_ed = process.extractOne(token, GEN_EDS.keys(), scorer=fuzz.partial_ratio)
        if gen_ed and gen_ed[1] > FUZZ_THRESH:
            self.advanced_query.gened_reqs = GEN_EDS[gen_ed[0]]
            return True
        return False

    def _match_subj_and_id_regex(self, token):
        pattern = re.compile(r'\s*([a-zA-Z]{2,4})\s*(\d{0,3})\s*')
        if pattern.match(token) and not ':' in token:
            self.advanced_query.subject, self.advanced_query.course_id = pattern.match(token).groups()
            if self.advanced_query.subject.upper() not in SUBJECTS:
                raise ValueError('Invalid subject: {}'.format(self.advanced_query.subject))
            self.advanced_query.subject = self.advanced_query.subject.upper()
            return True
        return False
    
    def _match_colon_args(self, token):
        pattern = re.compile(r'\s*([a-zA-Z]+)\s*:\s*(.*)\s*')
        if pattern.match(token):
            prefix, value = pattern.match(token).groups()
            prefix = prefix.lower()
            if prefix in COLON_ARGS['year']:
                if len(value) == 2:
                    value = '20' + value
                if value in YEARS:
                    self.advanced_query.year = value
                else:
                    raise ValueError('Invalid year: {}'.format(value))
            elif prefix in COLON_ARGS['semester']:
                semester = SEMESTER[value.lower()]
                if semester in TERMS[self.advanced_query.year]:
                    self.advanced_query.semester = semester
                else:
                    raise ValueError('Invalid semester: {}'.format(value))
            elif prefix in COLON_ARGS['pot']:
                self.advanced_query.part_of_term = value.upper()
            elif prefix in COLON_ARGS['subject']:
                self.advanced_query.subject = value.upper()
            elif prefix in COLON_ARGS['course_id']:
                self.advanced_query.course_id = value
            elif prefix in COLON_ARGS['course']:
                if self._match_subj_and_id_regex(value):
                    return True
            elif prefix in COLON_ARGS['crn']:
                self.advanced_query.crn = value
            elif prefix in COLON_ARGS['hours']:
                self.advanced_query.credit_hours = value
            elif prefix in COLON_ARGS['instructor']:
                self.advanced_query.instructor = value
            elif prefix in COLON_ARGS['gen_ed']:
                if value.upper() in GEN_ED_CODES:
                    self.advanced_query.gened_reqs = [GEN_ED_CODES[value.upper()]]
                else:
                    raise ValueError('Invalid gen-ed code: {}'.format(value))
            elif prefix in COLON_ARGS['is']:
                if value.lower() in IS_ARGS['online']:
                    self.advanced_query.online = True
                elif value.lower() in IS_ARGS['campus']:
                    self.advanced_query.on_campus = True
                elif value.lower() in IS_ARGS['open']:
                    self.advanced_query.open_sections = True
            else:
                return False
        self.advanced_query.keyword = token
        return True


def parse_advanced_query_string(input_string: str) -> Optional[AdvancedSearchParameters]:
    if not input_string:
        return None

    parser = AdvancedQueryStringParser(input_string)
    return parser.parse()

def main():
    input_string = 'nat sciences, phys, year: 2020, sem: fall, hrs:3'
    advanced_query = parse_advanced_query_string(input_string)
    print(str(advanced_query))

if __name__ == '__main__':
    main()
