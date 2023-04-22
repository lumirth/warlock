import json
from typing import List
from dataclasses import dataclass
import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from .models import Query, SimpleCourse, AdvancedSearchParameters, DetailedCourse
from .data_loader import gpa_dataframe
import javascript
import polars as pl

# Constants
UNIVERSITY_API_BASE_URL = "https://courses.illinois.edu/cisapp/explorer"

# Rate My Professors module
rmp = javascript.require("@mtucourses/rate-my-professors")
UNIVERSITY_ID = 'U2Nob29sLTExMTI='


def search_advanced(advanced_search: AdvancedSearchParameters) -> List[SimpleCourse]:
    # warlock_query = WarlockQuery(advanced_search)

    # query_params = warlock_query.to_query_params()

    # response = requests.get(
    #     f"{UNIVERSITY_API_BASE_URL}/schedule/courses",
    #     params=query_params
    # )
    # xml_data = response.text
    # root = ET.fromstring(xml_data)

    simple_courses = []
    # for course in root.findall(".//ns2:course", root.nsmap):
    #     simple_courses.append(SimpleCourse.from_xml_element(course))

    return simple_courses

def search_simple(query: str) -> List:
    advanced_search = AdvancedSearchParameters(simple_query=query)
    search_results = search_advanced(advanced_search)
    return search_results

courses = search_simple("Phys 325")
courses_json = [course.__dict__ for course in courses]
print(json.dumps(courses_json, indent=2))
