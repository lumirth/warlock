from .models import *
from fuzzywuzzy import fuzz, process
from typing import Optional
import glob
import os
import pickle
import re
import time

DEFAULT_YEAR = time.localtime().tm_year
DEFAULT_SEMESTER = "fall" if time.localtime().tm_mon > 3 else "spring"

FUZZ_THRESH = 85

def load_pickles(pickles_dir: str) -> dict:
    files = glob.glob(os.path.join(pickles_dir, '*.pkl'))
    pickles = {}
    for file in files:
        with open(file, 'rb') as f:
            pickles[os.path.basename(file)] = pickle.load(f)

    gen_eds = pickles.get("gen_eds_matching.pkl")
    gen_ed_codes = pickles.get("gen_ed_codes.pkl")
    subjects = pickles.get("subjects_matching.pkl")
    years = pickles.get("years.pkl")
    terms = pickles.get("terms.pkl")

    subjects_reverse = {v: v for k, v in subjects.items()}
    subjects = {**subjects, **subjects_reverse}
    subjects = {k.lower(): v.lower() for k, v in subjects.items()}
    gen_eds = {k.lower(): v.lower() for k, v in gen_eds.items()}
    gen_ed_codes = {k.lower(): v.lower() for k, v in gen_ed_codes.items()}

    return {
        "gen_eds": gen_eds,
        "gen_ed_codes": gen_ed_codes,
        "subjects": subjects,
        "years": years,
        "terms": terms,
    }
    
def parse_string_into_parameters(input_string: str, data: dict) -> Optional[Parameters]:
    if not input_string:
        return None

    tokens = input_string.split(",")
    advanced_query = Parameters()

    for token in tokens:
        advanced_query = _parse_token(token, advanced_query, data)

    _align_to_pattern(advanced_query, data)

    return advanced_query


def _align_to_pattern(advanced_query: Parameters, data: dict):
    # subject should be max 4 alphabetic characters, all caps
    if advanced_query.subject is not None:
        advanced_query.subject = advanced_query.subject.upper()
        if len(advanced_query.subject) > 4:
            advanced_query.subject = advanced_query.subject[:4]
        if advanced_query.subject not in data["subjects"].keys():
            subject = process.extractOne(
                advanced_query.subject,
                data["subjects"].keys(),
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
        if advanced_query.year not in data["years"]:
            raise ValueError("Year not found")
        advanced_query.year = int(advanced_query.year)
    # part_of_term must be in PART_OF_TERM
    if advanced_query.part_of_term is not None:
        if advanced_query.part_of_term.lower() not in PART_OF_TERM:
            raise ValueError("Part of term not found")
        advanced_query.part_of_term = PART_OF_TERM[advanced_query.part_of_term]
    if advanced_query.year is None:
        advanced_query.year = DEFAULT_YEAR
    if advanced_query.term is None:
        advanced_query.term = DEFAULT_SEMESTER

def _parse_colon_arguments(token: str, advanced_query: Parameters, data: dict) -> Parameters:
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
            if value in data["gen_ed_codes"]:
                value = data["gen_ed_codes"][value].upper()
            else:
                raise ValueError(f"Invalid gen ed code: {value}")
            advanced_query.gened_reqs.append(value)
            return advanced_query
    raise ValueError(f"Invalid colon argument: {key}")

def _parse_subject_and_course_number(token: str, advanced_query: Parameters, data: dict) -> Parameters:
    subject, course_number = re.match(r"^([a-zA-Z ]+)(?:\s+)?(\d+)$", token).groups()
    subject, course_number = subject.strip(), int(course_number)

    if course_number == 1:
        fuzzy_match = process.extractOne(
            subject,
            data["gen_eds"].keys(),
            scorer=fuzz.token_set_ratio,
            score_cutoff=FUZZ_THRESH,
        )
        if fuzzy_match is not None:
            fuzzy_match = fuzzy_match[0]
            if fuzzy_match in data["gen_eds"]:
                if advanced_query.gened_reqs is None:
                    advanced_query.gened_reqs = []
                advanced_query.gened_reqs.append(data["gen_eds"][fuzzy_match].upper())
                return advanced_query

    if subject not in data["subjects"]:
        subject = process.extractOne(
            subject,
            data["subjects"].keys(),
            scorer=fuzz.token_set_ratio,
            score_cutoff=FUZZ_THRESH,
        )
        if subject is None:
            raise ValueError("Subject not found")
        else:
            subject = subject[0]
    else:
        subject = data["subjects"][subject]

    advanced_query.subject = data["subjects"][subject].upper()
    advanced_query.course_id = course_number

    return advanced_query

def _parse_optional_digits_pattern(token: str, advanced_query: Parameters, data: dict) -> Parameters:
    subj_match = process.extractOne(token, data["subjects"].keys(), scorer=fuzz.token_set_ratio, score_cutoff=FUZZ_THRESH)
    gened_match = process.extractOne(token, data["gen_eds"].keys(), scorer=fuzz.token_set_ratio, score_cutoff=FUZZ_THRESH)

    subj_score = subj_match[1] if subj_match is not None else 0
    gened_score = gened_match[1] if gened_match is not None else 0

    if subj_score > 0 or gened_score > 0:
        if subj_score == gened_score:
            matches = [subj_match[0], gened_match[0]]
            best_match = process.extractOne(token,matches,scorer=fuzz.token_sort_ratio)
            if subj_match and best_match[0] == subj_match[0]:
                                advanced_query.subject = data["subjects"][subj_match[0]].upper()
            else:
                if advanced_query.gened_reqs is None:
                    advanced_query.gened_reqs = []
                advanced_query.gened_reqs.append(data["gen_eds"][gened_match[0]].upper())
        elif subj_score > gened_score:
            advanced_query.subject = data["subjects"][subj_match[0]].upper()
        else:
            if advanced_query.gened_reqs is None:
                advanced_query.gened_reqs = []
            advanced_query.gened_reqs.append(data["gen_eds"][gened_match[0]].upper())
    else:
        advanced_query.keyword = token

    return advanced_query

def _parse_token(token: str, advanced_query: Parameters, data: dict) -> Parameters:
    token = token.strip()
    token = token.lower()

    if not token:
        return advanced_query

    if ":" in token:
        return _parse_colon_arguments(token, advanced_query, data)

    if _token_is_crn(token):
        advanced_query.crn = token
        return advanced_query

    if _token_is_year(token, data):
        advanced_query.year = token
        return advanced_query

    if _token_is_semester(token):
        advanced_query.term = SEMESTER[token]
        return advanced_query

    if re.match(r"^([a-zA-Z ]+)(?:\s+)?(\d+)$", token):
        return _parse_subject_and_course_number(token, advanced_query, data)

    if re.match(r"^([a-zA-Z\- ]+)(?:\s+)?(\d+)?$", token):
        return _parse_optional_digits_pattern(token, advanced_query, data)

    return advanced_query

def _token_is_crn(token):
    if not token:
        return False

    if len(token) != 5:
        return False
    if not token.isdigit():
        return False

    return True


def _token_is_year(token, data):
    if token in data["years"]:
        return True


def _token_is_semester(token):
    if token.lower() in SEMESTER:
        return True
    
    
# These two dicts below must match fields of AdvancedSearchParameters
COLON_ARGS = {
    "year": ("year", "yr", "y"),
    "term": ("semester", "sem", "term", "s", "t"),
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
