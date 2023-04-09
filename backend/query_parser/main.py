import time
import re
import pickle
from fuzzywuzzy import fuzz, process
import os

DEBUG = True
DEFAULT_YEAR = time.localtime().tm_year
DEFAULT_SEMESTER = 'fall' if time.localtime().tm_mon > 3 else 'spring'

FUZZ_THRESH = 50

# unpickle unchanging data
PICKLES_DIR = 'pickles'
GEN_EDS = pickle.load(open(os.path.join(PICKLES_DIR, 'gen_eds.pkl'), 'rb'))
GEN_ED_CODES = pickle.load(open(os.path.join(PICKLES_DIR, 'gen_ed_codes.pkl'), 'rb'))
YEARS = pickle.load(open(os.path.join(PICKLES_DIR, 'years.pkl'), 'rb'))
SUBJECTS = pickle.load(open(os.path.join(PICKLES_DIR, 'subjects.pkl'), 'rb'))
TERMS = pickle.load(open(os.path.join(PICKLES_DIR, 'terms.pkl'), 'rb'))

class WarlockQuery:
    def __init__(self, query):
        self.query = query

        self.year = DEFAULT_YEAR
        self.semester = DEFAULT_SEMESTER
        self.pot = None
        self.subject = None
        self.course_id = None
        self.crn = None
        self.hours = None
        self.instructor = None
        self.gen_ed = None
        self.online_flag = None
        self.campus_flag = None
        self.open_flag = None
        self.keywords = None

        self._parse()
        
    def __str__(self) -> str:
        string = 'Query: \'{}\'\n'.format(self.query)
        attributes = [
            'year', 'semester', 'pot', 'subject', 'course_id', 'crn', 'hours',
            'instructor', 'gen_ed', 'online_flag', 'campus_flag', 'open_flag', 'keywords'
        ]
        max_attr_length = max(len(attr) for attr in attributes)
        for attr in attributes:
            value = getattr(self, attr)
            if value is not None:
                string += '  - {:<{}}: {}\n'.format(attr, max_attr_length, value)
        
        return string

    def _match_gen_ed_fuzzy(self, token):
        print('  - matching: gened fuzzy') if DEBUG else None
        gen_ed = process.extractOne(token, GEN_EDS.keys(), scorer=fuzz.token_sort_ratio)
        if gen_ed and gen_ed[1] > FUZZ_THRESH:
            self.gen_ed = GEN_EDS[gen_ed[0]]
            return True
        return False
    
    def _match_subj_and_id_regex(self, token):
        print('  - matching: subj and id fuzzy') if DEBUG else None
        pattern = re.compile(r'\s*([a-zA-Z]{2,4})\s*(\d{0,3})\s*')
        if pattern.match(token) and not ':' in token:
            self.subject, self.course_id = pattern.match(token).groups()
            # If subject was ever valid across all years, it will be in SUBJECTS
            # We could theoretically check if valid by year, but that would be
            # a lot of work for little gain
            if self.subject.upper() not in SUBJECTS:
                raise ValueError('Invalid subject: {}'.format(self.subject))
            self.subject = self.subject.upper()
            return True
        return False
    
    def _match_colon_args(self, token):
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
        pattern = re.compile(r'\s*([a-zA-Z]+)\s*:\s*(.*)\s*')
        if pattern.match(token):
            prefix, value = pattern.match(token).groups()
            prefix = prefix.lower()
            print('  - matching: {} = {}'.format(prefix, value)) if DEBUG else None
            if prefix in COLON_ARGS['year']:
                if len(value) == 2:
                    value = '20' + value
                if value in YEARS:
                    self.year = value
                else:
                    raise ValueError('Invalid year: {}'.format(value))
            elif prefix in COLON_ARGS['semester']:
                # NOTE: if user specifies term before year, and default year
                # contains term while intended doesn't, this will fail quietly
                semester = SEMESTER[value.lower()]
                if semester in TERMS[self.year]:
                    self.semester = semester
                else:
                    raise ValueError('Invalid semester: {}'.format(value))
            elif prefix in COLON_ARGS['pot']:
                # NOTE: we don't have error checking for this, so it'll fail
                # quietly if the user enters an invalid pot
                self.pot = value.upper()
            elif prefix in COLON_ARGS['subject']:
                self.subject = value.upper()
            elif prefix in COLON_ARGS['course_id']:
                self.course_id = value
            elif prefix in COLON_ARGS['course']:
                if self._match_subj_and_id_regex(value):
                    return True
            elif prefix in COLON_ARGS['crn']:
                self.crn = value
            elif prefix in COLON_ARGS['hours']:
                self.hours = int(value)
            elif prefix in COLON_ARGS['instructor']:
                self.instructor = value
            elif prefix in COLON_ARGS['gen_ed']:
                if value.upper() in GEN_ED_CODES:
                    self.gen_ed = GEN_ED_CODES[value.upper()]
                else:
                    raise ValueError('Invalid gen-ed code: {}'.format(value)) 
            elif prefix in COLON_ARGS['is']:
                if value.lower() in IS_ARGS['online']:
                    self.online_flag = True
                elif value.lower() in IS_ARGS['campus']:
                    self.campus_flag = True
                elif value.lower() in IS_ARGS['open']:
                    self.open_flag = True
            else:
                return False
        return True


    def _parse_token(self, token):
        print('+ parsing token: {}'.format(token)) if DEBUG else None
        if len(token) > 7:
            if self._match_gen_ed_fuzzy(token):
                return
        if not ':' in token:
            if self._match_subj_and_id_regex(token):
                return
        if token.isdigit() and len(token) == 5:
            print('matched crn') if DEBUG else None
            self.crn = token
            return
        if self._match_colon_args(token):
            return
        self.keywords = token

    def _parse(self):
        tokens = self.query.split(',')

        for token in tokens:
            self._parse_token(token)


def main():
    query = WarlockQuery('math 257, year:2021, semester:fall, is:online, is:open')
    print('==============================')
    print(query)


if __name__ == '__main__':
    main()
