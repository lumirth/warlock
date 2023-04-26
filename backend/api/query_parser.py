from api.courses import AdvancedSearchParameters
from fuzzywuzzy import fuzz, process
from typing import Optional
import os
import pickle
import re
import time

DEBUG = True
DEFAULT_YEAR = time.localtime().tm_year
DEFAULT_SEMESTER = "fall" if time.localtime().tm_mon > 3 else "spring"

FUZZ_THRESH = 85

# change directory to the directory of this file
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

PICKLES_DIR = "pickles"

# convert keys and values to lowercase. we change them to uppercase as appropriate later
gen_eds = pickle.load(open(os.path.join(PICKLES_DIR, "gen_eds_matching.pkl"), "rb"))
gen_ed_codes = pickle.load(open(os.path.join(PICKLES_DIR, "gen_ed_codes.pkl"), "rb"))
subjects = pickle.load(open(os.path.join(PICKLES_DIR, "subjects_matching.pkl"), "rb"))
subjects_reverse = {v: v for k, v in subjects.items()}
subjects = {**subjects, **subjects_reverse}
subjects = {k.lower(): v.lower() for k, v in subjects.items()}

# constants
GEN_EDS = {k.lower(): v.lower() for k, v in gen_eds.items()}
GEN_ED_CODES = {k.lower(): v.lower() for k, v in gen_ed_codes.items()}
YEARS = pickle.load(open(os.path.join(PICKLES_DIR, "years.pkl"), "rb"))
SUBJECTS = subjects
TERMS = pickle.load(open(os.path.join(PICKLES_DIR, "terms.pkl"), "rb"))

# These two dicts below must match fields of AdvancedSearchParameters
COLON_ARGS = {
    "year": ("year", "yr", "y"),
    "semester": ("semester", "sem", "term", "s", "t"),
    "subject": ("subject", "subj", "department", "dept", "d"),
    "course_id": ("course_id", "courseid", "id", "course", "number", "num", "n"),
    "crn": ("crn", "r"),
    "credit_hours": ("hours", "hrs", "hr", "h"),
    "instructor": ("instructor", "professor", "prof", "inst", "pr", "i"),
    "gened_reqs": ("gened_reqs", "gened", "gen-ed", "gen ed", "ge", "gen", "g"),
    "part_of_term": ("pot", "part", "part-of-term", "session", "p"),
    "keyword": ("keyword", "key", "k", "query", "q"),
}

IS_ARGS = {
    "online": ("online", "on", "o"),
    "on_campus": ("campus", "on-campus", "on campus", "oncampus", "c"),
    "open_sections": ("open", "o"),
}

SEMESTER = {
    "fa": "fall",
    "sp": "spring",
    "su": "summer",
    "wi": "winter",
    "fall": "fall",
    "spring": "spring",
    "summer": "summer",
    "winter": "winter",
    "fal": "fall",
    "spr": "spring",
    "sum": "summer",
    "win": "winter",
}

PART_OF_TERM = {
    "first": "A",
    "second": "B",
    "whole": "1",
    "full": "1",
    "a": "A",
    "b": "B",
    "all": "1",
    "first half": "A",
    "second half": "B",
    "1st": "A",
    "2nd": "B",
}


def parse_advanced_query_string(
    input_string: str,
) -> Optional[AdvancedSearchParameters]:
    if not input_string:
        return None

    tokens = input_string.split(",")
    advanced_query = AdvancedSearchParameters()

    for token in tokens:
        advanced_query = parse_token(token, advanced_query)

    align_to_pattern(advanced_query)

    return advanced_query


def align_to_pattern(advanced_query: AdvancedSearchParameters):
    # subject should be max 4 alphabetic characters, all caps
    if advanced_query.subject is not None:
        advanced_query.subject = advanced_query.subject.upper()
        if len(advanced_query.subject) > 4:
            advanced_query.subject = advanced_query.subject[:4]
        if advanced_query.subject not in SUBJECTS.keys():
            subject = process.extractOne(
                advanced_query.subject,
                SUBJECTS.keys(),
                scorer=fuzz.token_set_ratio,
                score_cutoff=FUZZ_THRESH,
            )
            if subject is None:
                raise ValueError("Subject not found")
    # semester should be one of the following: fall, spring, summer, winter
    if advanced_query.term is not None:
        advanced_query.term = SEMESTER[advanced_query.term]
    # year should be a 4 digit number in YEARS
    if advanced_query.year is not None:
        advanced_query.year = str(advanced_query.year)
        if advanced_query.year not in YEARS:
            raise ValueError("Year not found")
        advanced_query.year = int(advanced_query.year)
    # part_of_term must be in PART_OF_TERM
    if advanced_query.part_of_term is not None:
        if advanced_query.part_of_term.lower() not in PART_OF_TERM:
            raise ValueError("Part of term not found")
        advanced_query.part_of_term = PART_OF_TERM[advanced_query.part_of_term]


def parse_colon_arguments(token: str, advanced_query: AdvancedSearchParameters) -> AdvancedSearchParameters:
    key, value = token.split(":", 1)
    key, value = key.strip(), value.strip()
    if key in ("is"):
        for arg, aliases in IS_ARGS.items():
            if value in aliases:
                setattr(advanced_query, arg, True)
                return advanced_query
    for arg, aliases in COLON_ARGS.items():
        if key in aliases and arg not in ("gened_reqs"):
            setattr(advanced_query, arg, value)
            return advanced_query
        elif key in aliases and arg in ("gened_reqs"):
            if advanced_query.gened_reqs is None:
                advanced_query.gened_reqs = []
            if value in GEN_ED_CODES:
                value = GEN_ED_CODES[value].upper()
            else:
                raise ValueError(f"Invalid gen ed code: {value}")
            advanced_query.gened_reqs.append(value)
            return advanced_query
    raise ValueError(f"Invalid colon argument: {key}")


def parse_subject_and_course_number(token: str, advanced_query: AdvancedSearchParameters) -> AdvancedSearchParameters:
    subject, course_number = re.match(r"^([a-zA-Z ]+)(?:\s+)?(\d+)$", token).groups()
    subject, course_number = subject.strip(), int(course_number)

    if course_number == 1:
        fuzzy_match = process.extractOne(
            subject,
            GEN_EDS.keys(),
            scorer=fuzz.token_set_ratio,
            score_cutoff=FUZZ_THRESH,
        )
        if fuzzy_match is not None:
            fuzzy_match = fuzzy_match[0]
            if fuzzy_match in GEN_EDS:
                if advanced_query.gened_reqs is None:
                    advanced_query.gened_reqs = []
                advanced_query.gened_reqs.append(GEN_EDS[fuzzy_match].upper())
                return advanced_query

    if subject not in SUBJECTS:
        subject = process.extractOne(
            subject,
            SUBJECTS.keys(),
            scorer=fuzz.token_set_ratio,
            score_cutoff=FUZZ_THRESH,
        )
        if subject is None:
            raise ValueError("Subject not found")
        else:
            subject = subject[0]
    else:
        subject = SUBJECTS[subject]

    advanced_query.subject = SUBJECTS[subject].upper()
    advanced_query.course_id = course_number

    return advanced_query


def parse_optional_digits_pattern(token: str, advanced_query: AdvancedSearchParameters) -> AdvancedSearchParameters:
    # match token with subject and gen eds
    subj_match = process.extractOne(token, SUBJECTS.keys(), scorer=fuzz.token_set_ratio, score_cutoff=FUZZ_THRESH)
    gened_match = process.extractOne(token, GEN_EDS.keys(), scorer=fuzz.token_set_ratio, score_cutoff=FUZZ_THRESH)

    # check which it matches better
    subj_score = subj_match[1] if subj_match is not None else 0
    gened_score = gened_match[1] if gened_match is not None else 0

    if subj_score > 0 or gened_score > 0:
        if subj_score == gened_score:
            matches = [subj_match[0], gened_match[0]]
            best_match = process.extractOne(
                token,
                matches,
                scorer=fuzz.token_sort_ratio,
            )
            if subj_match and best_match[0] == subj_match[0]:
                advanced_query.subject = SUBJECTS[subj_match[0]].upper()
            else:
                if advanced_query.gened_reqs is None:
                    advanced_query.gened_reqs = []
                advanced_query.gened_reqs.append(GEN_EDS[gened_match[0]].upper())
        elif subj_score > gened_score:
            advanced_query.subject = SUBJECTS[subj_match[0]].upper()
        else:
            if advanced_query.gened_reqs is None:
                advanced_query.gened_reqs = []
            advanced_query.gened_reqs.append(GEN_EDS[gened_match[0]].upper())
    else:
        advanced_query.keyword = token

    return advanced_query


def parse_token(token: str, advanced_query: AdvancedSearchParameters) -> AdvancedSearchParameters:
    token = token.strip()
    token = token.lower()

    if not token:
        return advanced_query

    if ":" in token:
        return parse_colon_arguments(token, advanced_query)

    if token_is_crn(token):
        advanced_query.crn = token
        return advanced_query

    if token_is_year(token):
        advanced_query.year = token
        return advanced_query

    if token_is_semester(token):
        advanced_query.term = SEMESTER[token]
        return advanced_query

    if re.match(r"^([a-zA-Z ]+)(?:\s+)?(\d+)$", token):
        return parse_subject_and_course_number(token, advanced_query)

    if re.match(r"^([a-zA-Z\- ]+)(?:\s+)?(\d+)?$", token):
        return parse_optional_digits_pattern(token, advanced_query)

    return advanced_query


def token_is_crn(token):
    if not token:
        return False

    if len(token) != 5:
        return False
    if not token.isdigit():
        return False

    return True


def token_is_year(token):
    if token in YEARS:
        return True


def token_is_semester(token):
    if token.lower() in SEMESTER:
        return True


if __name__ == "__main__":
    for key, value in GEN_EDS.items():
        if key != value:
            print(f"{key}: {value}")
    print("---")
    example_queries = [
        "cs",
        "adv comp",
        "CS 222",
        "math257",
        "pysch 101",
        "MACS, western",
        "hrs:1, is:online",
        "gen:HUM, is:campus",
        "adv comp, pot:b",
        "prof: wade",
        "keyword: data",
        "life sciences",
        "natural sciences, quant1",
        "PSYC, non-western",
        "fall, 2021, cs 128",
        "anthropology, 2019",
        "2005, mathematics, hrs:2",
        "design lab",
        # "crn: 12345, gen ed: Humanities - Hist & Phil",
        # "id: 101, subj: ece, pot: first, instructor: John Smith",
    ]

    for query in example_queries:
        print(parse_advanced_query_string(query))
