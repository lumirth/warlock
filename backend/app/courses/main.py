from ..models import Course, Parameters, Section, Meeting, Instructor, GenEd
from .data import add_prof_ratings, add_gpa_data
from .filter import filter_courses_by_id, filter_courses_by_level, filter_courses_by_online_or_campus, filter_courses_by_gen_eds, filter_courses_by_credit_hours, filter_courses_by_part_of_term
# from .xml import get_course_xml, parse_simple_course
from typing import List, Union, Tuple
import asyncio
import polars as pl
import aiohttp
import xml.etree.ElementTree as ElementTree
from functools import lru_cache

async def search_courses(search_params: Parameters, professor_cache: dict, gpa_data: pl.DataFrame) -> List[Course]:
    print('searching courses')
    # turn the received search parameters into a AdvancedSearchParameters object if it isn't already
    if not isinstance(search_params, Parameters):
        search_params = Parameters(**search_params)
        
    detailed_courses = []
    simple_courses = []
    if search_params.subject is not None:
        print('searching by subject')
        print('getting course xml from dept')
        course_xml = await get_course_xml_from_dept(search_params)
        print('parsing simple courses from dept')
        detailed_courses = parse_simple_courses_from_dept(course_xml)
        print('Got this many courses:', len(detailed_courses))
        print('filtering courses')
        if search_params.course_id is not None:
            simple_courses_filtered = filter_courses_by_id(detailed_courses, search_params.course_id)
            detailed_courses = simple_courses_filtered
        print('This many after filtering by id:', len(detailed_courses))
        if search_params.course_level is not None:
            simple_courses_filtered = filter_courses_by_level(detailed_courses, search_params.course_level)
            detailed_courses = simple_courses_filtered
        print('This many after filtering by level:', len(detailed_courses))
            
        flag = "both"
        if search_params.online:
            flag = "online"
        if search_params.on_campus:
            flag = "campus"
        if search_params.online and search_params.on_campus:
            flag = "both"

        if search_params.gened_reqs is not None:
            detailed_courses = filter_courses_by_gen_eds(detailed_courses, search_params.gened_reqs, search_params.match_any_gened_reqs)
        print('This many after filtering by gen eds:', len(detailed_courses))
        if search_params.credit_hours is not None:
            detailed_courses = filter_courses_by_credit_hours(detailed_courses, search_params.credit_hours)
        print('This many after filtering by credit hours:', len(detailed_courses))
        
        print(search_params.part_of_term)
        if search_params.part_of_term is not None:
            detailed_courses = filter_courses_by_part_of_term(detailed_courses, search_params.part_of_term)
        
        detailed_courses = add_gpa_data(detailed_courses, gpa_data)
        print('This many after adding gpa data:', len(detailed_courses))
        await add_prof_ratings(detailed_courses, professor_cache=professor_cache)
        print('This many after adding prof ratings:', len(detailed_courses))
        print('done filtering courses')
    else:
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
        await add_prof_ratings(detailed_courses, professor_cache=professor_cache)
    print('returning courses')
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

async def get_course_xml_from_dept(search_params: Parameters) -> ElementTree.Element:
    base_url = "https://courses.illinois.edu/cisapp/explorer/schedule"
    endpoint = "{base_url}/{year}/{term}/{subject}.xml?mode=cascade".format(
        base_url=base_url,
        year=search_params.year,
        term=search_params.term,
        subject=search_params.subject,
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint) as response:
            response.raise_for_status()
            content = await response.read()
    return ElementTree.fromstring(content)

def parse_simple_courses_from_dept(department: ElementTree.Element) -> List[Course]:
    courses = []

    for cascading_course in department.findall(".//cascadingCourse"):
        course_id = cascading_course.get("id") 
        label = cascading_course.find("label").text
        description = cascading_course.find("description").text
        credit_hours = cascading_course.find("creditHours").text
        href = cascading_course.get("href")

        sections = []
        for detailed_section in cascading_course.findall(".//detailedSection"):
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

                meetings.append(Meeting(typeCode=type_code, start=start, end=end, daysOfTheWeek=days_of_the_week,
                                        roomNumber=room_number, buildingName=building_name, instructors=instructors))

            sections.append(Section(id=section_id, sectionNumber=section_number, meetings=meetings, partOfTerm=part_of_term))

        gen_ed_attributes = []
        for category in cascading_course.findall(".//genEdCategories/category"):
            gen_ed_id = category.get("id")
            gen_ed_description = category.find("description").text
            gen_ed_attributes.append(GenEd(id=gen_ed_id, name=gen_ed_description))

        courses.append(Course(id=course_id, label=label, description=description, creditHours=credit_hours, href=href, 
                              sections=sections, genEdAttributes=gen_ed_attributes))

    return courses

async def get_course_xml(query_params: dict) -> ElementTree.Element:
    base_url = "https://courses.illinois.edu/cisapp/explorer/schedule"
    courses_endpoint = f"{base_url}/courses.xml"
    async with aiohttp.ClientSession() as session:
        async with session.get(courses_endpoint, params=query_params) as response:
            print(response.url)
            response.raise_for_status()
            content = await response.read()
    return ElementTree.fromstring(content)

def parse_simple_course(course: ElementTree.Element) -> Course:
    parents = course.find("parents")
    return Course(
        year=parents.find("calendarYear").attrib["id"] if parents.find("calendarYear") is not None else None,
        term=parents.find("term").text.split(" ")[0] if parents.find("term") is not None else None,
        subject=parents.find("subject").text if parents.find("subject") is not None else None,
        id=course.get("id"),
        label=course.find("label").text,
        description=course.find("description").text if course.find("description") is not None else None,
        creditHours=course.find("creditHours").text,
        href=course.get("href"),
        sectionDegreeAttributes=course.find("sectionDegreeAttributes").text if course.find("sectionDegreeAttributes") is not None else None,
        courseSectionInformation=course.find("courseSectionInformation").text if course.find("courseSectionInformation") is not None else None,
        genEdCategories=[genEdCategory.text for genEdCategory in course.findall(".//genEdCategory")] if course.findall(".//genEdCategory") is not None else None,
    )

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

