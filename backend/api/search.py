import json
from typing import List, Union
from dataclasses import dataclass
import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from api.courses import SimpleCourse, AdvancedSearchParameters
from api.courses import search_courses
from api.courses import initialize_professor_cache, save_professor_cache
from api.query_parser import parse_advanced_query_string
import polars as pl
import asyncio
import pydantic

# Constants
UNIVERSITY_API_BASE_URL = "https://courses.illinois.edu/cisapp/explorer"

def search_advanced(params: AdvancedSearchParameters) -> Union[List[SimpleCourse], SimpleCourse]:
    return []

def search_simple(query: str, professor_cache, gpa_data) -> List[SimpleCourse]:
    print('Parsing query')
    query_obj = parse_advanced_query_string(query)
    print('Searching courses')
    results = asyncio.run(search_courses(query_obj, professor_cache=professor_cache, gpa_data=gpa_data))
    # print(results)
    from api.try_searching_script import print_courses
    print_courses(results)
    return results

# courses = search_simple("Phys 325")
# courses_json = [course.__dict__ for course in courses]
# print(json.dumps(courses_json, indent=2))
