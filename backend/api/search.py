import json
from typing import List, Union
from dataclasses import dataclass
import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from api.courses import SimpleCourse, AdvancedSearchParameters
from api.courses import gpa_dataframe
from api.query_parser import parse_advanced_query_string
import polars as pl

# Constants
UNIVERSITY_API_BASE_URL = "https://courses.illinois.edu/cisapp/explorer"

def search_advanced(params: AdvancedSearchParameters) -> Union[List[SimpleCourse], SimpleCourse]:
    courses = []
    return courses

def search_simple(query: str) -> List[SimpleCourse]:
    results = search_advanced(parse_advanced_query_string(query))
    courses = []
    return courses

# courses = search_simple("Phys 325")
# courses_json = [course.__dict__ for course in courses]
# print(json.dumps(courses_json, indent=2))
