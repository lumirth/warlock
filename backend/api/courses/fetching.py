from .parse import parse_simple_course, parse_detailed_section
from .data import add_gpa_data, add_prof_ratings
from .filtering import filter_courses_by_id, filter_courses_by_level, filter_courses_by_online_or_campus
from .models import SimpleCourse, AdvancedSearchParameters, DetailedSection
from typing import Tuple, List
from xml.etree import ElementTree
import aiohttp
import asyncio


async def prepare_query_params(search_params: AdvancedSearchParameters) -> dict:
    query_params = {
        "year": search_params.year,
        "term": search_params.term,
        # "sectionTypeCode": "ONL" if search_params.online else None,
        "subject": search_params.subject,
        "collegeCode": search_params.college,
        "creditHours": search_params.credit_hours,
        "gened": " ".join(search_params.gened_reqs) if search_params.gened_reqs and not search_params.match_any_gened_reqs else None,
        "instructor": search_params.instructor if search_params.instructor else None,
        "sessionId": search_params.part_of_term,
        "qs": search_params.keyword if search_params.keyword_type == "qs" else None,
        "qp": search_params.keyword if search_params.keyword_type == "qp" else None,
        "qw_a": search_params.keyword if search_params.keyword_type == "qw_a" else None,
        "qw_o": search_params.keyword if search_params.keyword_type == "qw_o" else None,
    }
    return {k: v for k, v in query_params.items() if v is not None}


async def get_course_xml(query_params: dict) -> ElementTree.Element:
    base_url = "https://courses.illinois.edu/cisapp/explorer/schedule"
    courses_endpoint = f"{base_url}/courses.xml"
    async with aiohttp.ClientSession() as session:
        async with session.get(courses_endpoint, params=query_params) as response:
            print(response.url)
            response.raise_for_status()
            content = await response.read()
    return ElementTree.fromstring(content)


async def get_course_details(simple_course: SimpleCourse) -> SimpleCourse:
    async with aiohttp.ClientSession() as session:
        async with session.get(simple_course.href, params={"mode": "cascade"}) as response:
            response.raise_for_status()
            content = await response.read()
    course_xml_data = ElementTree.fromstring(content)
    detailed_sections = [parse_detailed_section(detailed_section) for detailed_section in course_xml_data.findall(".//detailedSection")]
    simple_course.sections = detailed_sections
    return simple_course


async def search_courses(search_params: AdvancedSearchParameters, professor_cache, gpa_data) -> Tuple[List[SimpleCourse], List[List[DetailedSection]]]:
    # turn the received search parameters into a AdvancedSearchParameters object if it isn't already
    if not isinstance(search_params, AdvancedSearchParameters):
        search_params = AdvancedSearchParameters(**search_params)
    query_params = await prepare_query_params(search_params)
    course_xml = await get_course_xml(query_params)

    simple_courses = list(map(parse_simple_course, course_xml.findall(".//course")))
    detailed_courses = await asyncio.gather(*(get_course_details(course) for course in simple_courses))

    if search_params.course_id is not None:
        simple_courses_filtered = filter_courses_by_id(detailed_courses, search_params.course_id)
        detailed_courses = simple_courses_filtered

    if search_params.course_level is not None:
        simple_courses_filtered = filter_courses_by_level(detailed_courses, search_params.course_level)
        detailed_courses = simple_courses_filtered

    flag = "both"
    if search_params.online:
        flag = "online"
    if search_params.on_campus:
        flag = "campus"
    if search_params.online and search_params.on_campus:
        flag = "both"

    detailed_courses = filter_courses_by_online_or_campus(detailed_courses, flag=flag)

    detailed_courses = add_gpa_data(detailed_courses, gpa_data)
    simple_courses = await add_prof_ratings(simple_courses, professor_cache)

    return detailed_courses
