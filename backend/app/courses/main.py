from ..models import Course, Parameters, Section, Meeting, Instructor, GenEd
from ..utils import logger, log_time_func, log_time_async
from .data import add_prof_ratings, add_gpa_data
from .filter import (
    filter_courses_by_credit_hours,
    filter_courses_by_gen_eds,
    filter_courses_by_id,
    filter_courses_by_instructor_last_name,
    filter_courses_by_keyword,
    filter_courses_by_level,
    filter_courses_by_online_or_campus,
    filter_courses_by_part_of_term,
)
from typing import List, Union, Tuple
import aiohttp
import asyncio
import polars as pl
import time
import xml.etree.ElementTree as ElementTree

# TODO: spring cleaning. it's a mess in here
# TODO: fix searching for gen ed categories (because filtering only works on subcategories)
# TODO: fix match all vs match any gen ed reqs, it doesnt work at all right now

SECTION_DEGREE_ATTRIBUTES_GEN_EDS = {
    "Composition I": "COMP1",
    "Advanced Composition": "1CLL",
    "Quantitative Reasoning I": "1QR1",
    "Quantitative Reasoning II": "1QR2",
    "Nat Sci & Tech - Life Sciences": "1LS",
    "Nat Sci & Tech - Phys Sciences": "1PS",
    "Humanities - Hist & Phil": "1HP",
    "Humanities - Lit & Arts": "1LA",
    "Cultural Studies - Western": "1WCC",
    "Cultural Studies - Non-West": "1NW",
    "Cultural Studies - US Minority": "1US",
    "Social & Beh Sci - Soc Sci": "1SS",
    "Social & Beh Sci - Beh Sci": "1BSC",
}

async def search_courses(search_params: Parameters, gpa_data: pl.DataFrame) -> List[Course]:
    search_params = validate_and_prepare_search_params(search_params)
    courses = await get_courses_based_on_search_params(search_params, gpa_data)
    return courses


def validate_and_prepare_search_params(search_params: Parameters) -> Parameters:
    if not isinstance(search_params, Parameters):
        search_params = Parameters(**search_params)

    if search_params.course_id is not None and len(str(search_params.course_id)) != 3:
        search_params.course_level = str(search_params.course_id)[0]
        search_params.course_id = None

    return search_params


async def get_courses_based_on_search_params(search_params: Parameters, gpa_data: pl.DataFrame) -> List[Course]:
    if search_params.crn is not None:
        return await get_courses_by_crn(search_params, gpa_data)

    if search_params.course_id is not None and search_params.subject is not None:
        return await get_single_course(search_params, gpa_data)

    return await get_courses_by_query_params(search_params, gpa_data)


@log_time_func
async def get_courses_by_crn(search_params: Parameters, gpa_data: pl.DataFrame) -> List[Course]:
    course_xml = await get_section_xml_from_crn(search_params)
    course = await parse_course_from_section(course_xml)
    courses = [course]
    courses = add_gpa_data(courses, gpa_data)
    return courses


@log_time_func
async def get_single_course(search_params: Parameters, gpa_data: pl.DataFrame) -> List[Course]:
    course_xml = await get_single_course_xml(search_params)
    course = parse_course_from_full_course(course_xml)
    courses = [course]
    courses = add_gpa_data(courses, gpa_data)
    return courses


@log_time_func
async def get_courses_by_query_params(search_params: Parameters, gpa_data: pl.DataFrame) -> List[Course]:
    async with log_time_async("prepare_query_params"):
        query_params = await prepare_query_params(search_params)

    async with log_time_async("get_course_search_xml"):
        course_xml = await get_course_search_xml(query_params)

    async with log_time_async("parse_simple_course"):
        simple_courses = list(map(parse_simple_course, course_xml.findall(".//course")))

    async with log_time_async("filter_courses_by_id"):
        if search_params.course_id is not None:
            simple_courses = filter_courses_by_id(simple_courses, search_params.course_id)

        if search_params.course_level is not None:
            simple_courses = filter_courses_by_level(simple_courses, search_params.course_level)

    async with log_time_async("add_gpa_data"):
        simple_courses = add_gpa_data(simple_courses, gpa_data)

    return simple_courses


async def get_course_search_xml(query_params: dict) -> ElementTree.Element:
    base_url = "https://courses.illinois.edu/cisapp/explorer/schedule"
    courses_endpoint = f"{base_url}/courses.xml"
    async with aiohttp.ClientSession() as session:
        async with session.get(courses_endpoint, params=query_params) as response:
            logger.info("Getting course xml, URL:")
            logger.info(response.url)
            response.raise_for_status()
            content = await response.read()
    return ElementTree.fromstring(content)


async def get_section_xml_from_crn(search_params: Parameters) -> ElementTree.Element:
    base_url = "https://courses.illinois.edu/cisapp/explorer/schedule"
    courses_endpoint = f"{base_url}/sections.xml"
    params = {
        "year": search_params.year,
        "term": search_params.term,
        "crn": search_params.crn,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(courses_endpoint, params=params) as response:
            logger.info("Getting section xml from crn, URL:")
            logger.info(response.url)
            response.raise_for_status()
            content = await response.read()
    return ElementTree.fromstring(content)


async def get_single_course_xml(search_params: Parameters) -> ElementTree.Element:
    base_url = "https://courses.illinois.edu/cisapp/explorer/schedule"
    endpoint = "{base_url}/{year}/{term}/{subject}/{course_id}.xml?mode=cascade".format(
        base_url=base_url,
        year=search_params.year,
        term=search_params.term,
        subject=search_params.subject,
        course_id=search_params.course_id,
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint) as response:
            logger.info("Getting single course xml, URL:")
            logger.info(response.url)
            response.raise_for_status()
            content = await response.read()
    return ElementTree.fromstring(content)


async def parse_course_from_section(section: ElementTree.Element) -> List[Course]:
    sections = section.find("sections")
    section = sections.find("section")
    parents = section.find("parents")
    href = parents.find("course").get("href")
    async with aiohttp.ClientSession() as session:
        async with session.get(href + "?mode=cascade") as response:
            logger.info("Getting single course xml from section, URL:")
            logger.info(response.url)
            response.raise_for_status()
            content = await response.read()
    course_xml_data = ElementTree.fromstring(content)
    course = parse_course_from_full_course(course_xml_data)
    return course


def parse_course_from_full_course(course: ElementTree.Element) -> Course:
    course_id = course.get("id")
    label = course.find("label").text
    description = course.find("description").text
    credit_hours = course.find("creditHours").text[0]
    href = course.get("href")
    year = course.find("parents").find("calendarYear").attrib["id"]
    term = course.find("parents").find("term").text.split(" ")[0]

    sections = []
    for detailed_section in course.findall(".//detailedSection"):
        section_id = detailed_section.get("id")
        section_number = detailed_section.find("sectionNumber").text if detailed_section.find("sectionNumber") is not None else None
        part_of_term = detailed_section.find("partOfTerm").text if detailed_section.find("partOfTerm") is not None else None
        meetings = []
        for meeting in detailed_section.findall(".//meeting"):
            type_code = meeting.find("type").get("code") if meeting.find("type") is not None else None
            start = meeting.find("start").text if meeting.find("start") is not None else None
            end = meeting.find("end").text if meeting.find("end") is not None else None
            days_of_the_week = meeting.find("daysOfTheWeek").text if meeting.find("daysOfTheWeek") is not None else None
            room_number = meeting.find("roomNumber").text if meeting.find("roomNumber") is not None else None
            building_name = meeting.find("buildingName").text if meeting.find("buildingName") is not None else None

            instructors = []
            for instructor in meeting.findall(".//instructor"):
                last_name = instructor.get("lastName")
                first_name = instructor.get("firstName")
                instructors.append(Instructor(lastName=last_name, firstName=first_name))

            meetings.append(Meeting(typeCode=type_code, start=start, end=end, daysOfTheWeek=days_of_the_week, roomNumber=room_number, buildingName=building_name, instructors=instructors))

        sections.append(Section(id=section_id, sectionNumber=section_number, meetings=meetings, partOfTerm=part_of_term))

    # get gen ed attributes
    gen_ed_attributes = []
    for attribute in course.findall(".//genEdAttribute"):
        code = attribute.attrib["code"] if attribute.attrib["code"] is not None else None
        gen_ed_attributes.append(GenEd(id=code, name=attribute.text))

    return Course(id=course_id, label=label, description=description, creditHours=credit_hours, href=href, sections=sections, genEdAttributes=gen_ed_attributes, term=term, year=year)


def parse_simple_course(course: ElementTree.Element) -> Course:
    parents = course.find("parents")
    course = Course(
        year=parents.find("calendarYear").attrib["id"] if parents.find("calendarYear") is not None else None,
        term=parents.find("term").text.split(" ")[0] if parents.find("term") is not None else None,
        subject=parents.find("subject").text if parents.find("subject") is not None else None,
        id=course.get("id"),
        label=course.find("label").text,
        description=course.find("description").text if course.find("description") is not None else None,
        creditHours=course.find("creditHours").text[0] if course.find("creditHours") is not None else None,
        href=course.get("href"),
        sectionRegistrationNotes=course.find("sectionRegistrationNotes").text if course.find("sectionRegistrationNotes") is not None else None,
        sectionDegreeAttributes=course.find("sectionDegreeAttributes").text if course.find("sectionDegreeAttributes") is not None else None,
        courseSectionInformation=course.find("courseSectionInformation").text if course.find("courseSectionInformation") is not None else None,
    )

    # check sectionDegreeAttributes for any matches from the pickles["gen_eds"] dictionary and save them to the GenEds field
    sectionDegreeAttributes = course.sectionDegreeAttributes
    if sectionDegreeAttributes is not None:
        course.genEdAttributes = []
        for gen_ed in SECTION_DEGREE_ATTRIBUTES_GEN_EDS:
            if gen_ed in sectionDegreeAttributes:
                if gen_ed == "Quantitative Reasoning I" and "Quantitative Reasoning II" in sectionDegreeAttributes:
                    continue
                sectionDegreeAttributes = sectionDegreeAttributes.replace(gen_ed, "")
                course.genEdAttributes.append(GenEd(id=SECTION_DEGREE_ATTRIBUTES_GEN_EDS[gen_ed], name=gen_ed))
    return course


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
        "subject": search_params.subject,
        # "collegeCode": search_params.college,
        "creditHours": search_params.credit_hours,
        "gened": " ".join(search_params.gened_reqs) if search_params.gened_reqs and not search_params.match_any_gened_reqs else None,
        "instructor": search_params.instructor if search_params.instructor else None,
        "sessionId": search_params.part_of_term,
        "sectionTypeCode": "ONL" if search_params.online else None,
        "enrollmentStatus": "Open" if search_params.open_sections else None,
        # TODO: replace "on campus" with "section type code" in parameters
        "qs": search_params.keyword if search_params.keyword_type == "qs" else None,
        "qp": search_params.keyword if search_params.keyword_type == "qp" else None,
        "qw_a": search_params.keyword if search_params.keyword_type == "qw_a" else None,
        "qw_o": search_params.keyword if search_params.keyword_type == "qw_o" else None,
    }
    return {k: v for k, v in query_params.items() if v is not None}
