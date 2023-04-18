import json
from typing import List
from dataclasses import dataclass
import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from models import Query, SimpleCourse, AdvancedSearchParameters, DetailedCourse
from data_loader import gpa_dataframe
import javascript
import polars as pl
from query_parser import WarlockQuery

# Constants
UNIVERSITY_API_BASE_URL = "https://courses.illinois.edu/cisapp/explorer"

# Rate My Professors module
rmp = javascript.require("@mtucourses/rate-my-professors")
UNIVERSITY_ID = 'U2Nob29sLTExMTI='


def search_simple(query: str) -> List:
    # Create a WarlockQuery object for parsing
    warlock_query = WarlockQuery(Query(simple_query=query))
    print(str(warlock_query))
    # Implement the logic for simple search
    response = requests.get(
        f"{UNIVERSITY_API_BASE_URL}/schedule/courses.xml",
        params={
            "year": warlock_query.year,
            "term": warlock_query.semester,
            "subject": warlock_query.subject,
            "qs": warlock_query.keywords,
        },
    )
    # print request URL:
    print(response.url)
    xml_data = response.text
    
    # Parse the XML data
    root = ET.fromstring(xml_data)

    # Use the root element to find the 'courses' element
    courses_element = root.find("courses")

    # Use the 'courses' element to find all 'course' elements
    simple_courses = []
    if courses_element is not None:
        xml_courses = courses_element.findall("course")
        for course in xml_courses:
            # Process the course element (e.g., create SimpleCourse objects)
            simple_course = SimpleCourse.from_xml_element(course)
            
            # Split the subject and number from the ID
            subject, number = course.attrib["id"].split()

            # Query the GPA dataframe to find the average GPA for the course across all semesters
            
            gpa_data = gpa_dataframe.with_columns(
                Subject=gpa_dataframe["Subject"].cast(str),
                Number=gpa_dataframe["Number"].cast(str),
            )

            course_gpa_df = gpa_data.filter((gpa_data["Subject"] == subject) & (gpa_data["Number"] == number))

            # Replace the following line with the shape attribute check:
            # if not course_gpa_df.empty:
            if course_gpa_df.shape[0] > 0:
                course_gpa_average = course_gpa_df["GPA"].mean()
                simple_course.gpa_average = round(course_gpa_average, 2) if not course_gpa_average is None else None
            else:
                simple_course.gpa_average = None
            
            simple_courses.append(simple_course)
            
    return simple_courses


def search_advanced(advanced_search: AdvancedSearchParameters) -> List[SimpleCourse]:
    # Implement the logic for advanced search
    query_params = advanced_search.to_query_params()

    response = requests.get(
        f"{UNIVERSITY_API_BASE_URL}/schedule/courses",
        params=query_params
    )
    xml_data = response.text
    root = ET.fromstring(xml_data)

    simple_courses = []
    for course in root.findall(".//ns2:course", root.nsmap):
        simple_courses.append(SimpleCourse.from_xml_element(course))

    return simple_courses

# Example usage of the search_simple function
courses = search_simple("Phys 325")
courses_json = [course.__dict__ for course in courses]
print(json.dumps(courses_json, indent=2))

