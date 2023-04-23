import json
from typing import List
from dataclasses import dataclass
import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from api.models import Query, SimpleCourse, AdvancedSearchParameters, DetailedCourse
from api.data_loader import gpa_dataframe
from api.query_parser import parse_advanced_query_string
import javascript
import polars as pl

# Constants
UNIVERSITY_API_BASE_URL = "https://courses.illinois.edu/cisapp/explorer"

# Rate My Professors module
rmp = javascript.require("@mtucourses/rate-my-professors")
UNIVERSITY_ID = 'U2Nob29sLTExMTI='


def search_advanced(advanced_search: AdvancedSearchParameters) -> List[SimpleCourse]:
    courses = []
    # TODO: implement flow control for different endpoints based on parameters
    return courses

def search_simple(query: str) -> List[SimpleCourse]:
    results = search_advanced(parse_advanced_query_string(query))
    courses = []
    return courses

# courses = search_simple("Phys 325")
# courses_json = [course.__dict__ for course in courses]
# print(json.dumps(courses_json, indent=2))
