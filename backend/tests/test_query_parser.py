import os
import sys
import pickle
from typing import Optional
import pytest

# Add the backend/api directory to sys.path so we can import the query_parser module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'api')))

from api.query_parser import (
    parse_advanced_query_string,
    align_to_pattern,
    parse_colon_arguments,
    parse_subject_and_course_number,
    parse_optional_digits_pattern,
    parse_token,
    token_is_crn,
    token_is_year,
    token_is_semester,
)
from api.models import AdvancedSearchParameters


def test_parse_advanced_query_string():
    query = "sp, 2021, cs 2"
    result = parse_advanced_query_string(query)

    assert isinstance(result, AdvancedSearchParameters)
    assert result.year == 2021
    assert result.semester == 'spring'
    assert result.subject == 'CS'
    assert result.course_id == 2

    query = ""
    result = parse_advanced_query_string(query)

    assert result is None


def test_align_to_pattern():
    advanced_query = AdvancedSearchParameters(subject="cs", semester="sp", year='2021', part_of_term="first")

    align_to_pattern(advanced_query)

    assert advanced_query.subject == "CS"
    assert advanced_query.semester == "spring"
    assert advanced_query.year == 2021
    assert advanced_query.part_of_term == "A"

    with pytest.raises(ValueError):
        advanced_query.subject = "invalid_subject"
        align_to_pattern(advanced_query)


def test_parse_colon_arguments():
    # Test the function with various colon arguments
    pass  # Add test cases for each colon argument


def test_parse_subject_and_course_number():
    token = "CS 225"
    advanced_query = AdvancedSearchParameters()

    result = parse_subject_and_course_number(token, advanced_query)

    assert result.subject == "CS"
    assert result.course_id == 225


def test_parse_optional_digits_pattern():
    token = "cs"
    advanced_query = AdvancedSearchParameters()

    result = parse_optional_digits_pattern(token, advanced_query)

    assert result.subject == "CS"


def test_parse_token():
    token = "sp"
    advanced_query = AdvancedSearchParameters()

    result = parse_token(token, advanced_query)

    assert result.semester == "spring"


def test_token_is_crn():
    assert token_is_crn("12345")
    assert not token_is_crn("abcd")


def test_token_is_year():
    assert token_is_year('2021')
    assert not token_is_year('1000')


def test_token_is_semester():
    assert token_is_semester("sp")
    assert not token_is_semester("invalid")
    
def test_parse_advanced_query_string_fuzzy():
    # Test subject matching with slight typos and variations
    query1 = parse_advanced_query_string("sp, 2021, comp scii 225")
    assert query1.subject == 'CS'
    assert query1.course_id == 225
    assert query1.year == 2021
    assert query1.semester == 'spring'

    # Test gened_reqs matching with slight typos and variations
    query2 = parse_advanced_query_string("compossition 1")
    assert 'COMP1' in query2.gened_reqs

    query3 = parse_advanced_query_string("adv comp")
    assert '1CLL' in query3.gened_reqs

    query4 = parse_advanced_query_string("literature and the arts")
    assert '1LA' in query4.gened_reqs

    # Test semester matching with slight typos and variations
    query5 = parse_advanced_query_string("spr")
    assert query5.semester == 'spring'

    query6 = parse_advanced_query_string("win")
    assert query6.semester == 'winter'

    # Test part_of_term matching with slight typos and variations
    query7 = parse_advanced_query_string("pot:1st")
    assert query7.part_of_term == 'A'

    query8 = parse_advanced_query_string("p:second half")
    assert query8.part_of_term == 'B'

test_parse_advanced_query_string()

