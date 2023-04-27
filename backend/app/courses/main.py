from ..models import Course, Parameters, Section, Meeting, Instructor
from .data import add_prof_ratings, add_gpa_data
from .filter import filter_courses_by_id, filter_courses_by_level, filter_courses_by_online_or_campus
from .xml import get_course_xml, parse_simple_course
from typing import List, Union, Tuple
import asyncio
import polars as pl
import aiohttp
import xml.etree.ElementTree as ElementTree

async def search_courses(search_params: Parameters, professor_cache: dict, gpa_data: pl.DataFrame) -> List[Course]:
    # turn the received search parameters into a AdvancedSearchParameters object if it isn't already
    if not isinstance(search_params, Parameters):
        search_params = Parameters(**search_params)
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
    simple_courses = await add_prof_ratings(simple_courses, professor_cache=professor_cache)

    return detailed_courses


async def get_course_details(simple_course: Course) -> Course:
    async with aiohttp.ClientSession() as session:
        async with session.get(simple_course.href, params={"mode": "cascade"}) as response:
            response.raise_for_status()
            content = await response.read()
    course_xml_data = ElementTree.fromstring(content)
    detailed_sections = [parse_detailed_section(detailed_section) for detailed_section in course_xml_data.findall(".//detailedSection")]
    simple_course.sections = detailed_sections
    return simple_course

def parse_detailed_section(detailed_section: ElementTree.Element) -> Section:
    section = Section(
        id=detailed_section.get("id"),
        sectionNumber=detailed_section.find("sectionNumber").text if detailed_section.find("sectionNumber") is not None else None,
        statusCode=detailed_section.find("statusCode").text,
        partOfTerm=detailed_section.find("partOfTerm").text if detailed_section.find("partOfTerm") is not None else None,
        sectionStatusCode=detailed_section.find("sectionStatusCode").text,
        enrollmentStatus=detailed_section.find("enrollmentStatus").text,
        startDate=detailed_section.find("startDate").text if detailed_section.find("startDate") is not None else None,
        endDate=detailed_section.find("endDate").text if detailed_section.find("endDate") is not None else None,
        meetings=[],
    )
    for meeting in detailed_section.findall(".//meeting"):
        section.meetings.append(parse_meeting(meeting))
    return section


def parse_meeting(meeting: ElementTree.Element) -> Meeting:
    meeting_obj = Meeting(
        typeCode=meeting.find("type").attrib["code"] if meeting.find("type") is not None else None,
        typeDesc=meeting.find("type").text if meeting.find("type") is not None else None,
        start=meeting.find("start").text,
        end=meeting.find("end").text if meeting.find("end") is not None else None,
        daysOfTheWeek=meeting.find("daysOfTheWeek").text if meeting.find("daysOfTheWeek") is not None else None,
        roomNumber=meeting.find("roomNumber").text if meeting.find("roomNumber") is not None else None,
        buildingName=meeting.find("buildingName").text if meeting.find("buildingName") is not None else None,
        instructors=[],
    )
    for instructor in meeting.findall(".//instructor"):
        meeting_obj.instructors.append(parse_instructor(instructor))
    return meeting_obj


def parse_instructor(instructor: ElementTree.Element) -> Instructor:
    return Instructor(lastName=instructor.get("lastName"), firstName=instructor.get("firstName"))


async def prepare_query_params(search_params: Parameters) -> dict:
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