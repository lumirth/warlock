import requests
from typing import List, Tuple
from xml.etree import ElementTree
from models import SimpleCourse, DetailedSection, AdvancedSearchParameters, Instructor, Meeting
import polars as pl
from data_loader import gpa_dataframe
import asyncio
import aiohttp
import rmp
import time

time_spent_getting_profs = 0
time_spent_getting_ratings = 0
rating_count = 0


async def prepare_query_params(search_params: AdvancedSearchParameters) -> dict:
    query_params = {
        "year": search_params.year,
        "term": search_params.term,
        "sectionTypeCode": "ONL" if search_params.online else None,
        "subject": search_params.subject,
        "collegeCode": search_params.college,
        "creditHours": search_params.credit_hours,
        "gened": " ".join(search_params.gened_reqs) if search_params.gened_reqs else None,
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

def get_list_of_instructors(simple_course: SimpleCourse) -> List[str]:
    instructors = set()
    for section in simple_course.sections:
        for meeting in section.meetings:
            for instructor in meeting.instructors:
                instructors.add(f"{instructor.firstName} {instructor.lastName}")
    return list(instructors)

async def add_prof_ratings(simple_courses: List[SimpleCourse]) -> List[SimpleCourse]:
    global time_spent_getting_profs
    global time_spent_getting_ratings
    global rating_count
    for course in simple_courses:
        start = time.time()
        instructor_names = get_list_of_instructors(course)
        end = time.time()
        time_spent_getting_profs += end - start
        
        start = time.time()
        instructor_data = await rmp.get_ratings_for_teachers(instructor_names)
        end = time.time()
        time_spent_getting_ratings += end - start

        total_rating = 0
        num_ratings = 0

        for instructor in instructor_data:
            if instructor is not None:
                total_rating += instructor["avgRating"] * instructor["numRatings"]
                num_ratings += instructor["numRatings"]

        if num_ratings > 0:
            course.prof_average = total_rating / num_ratings
        else:
            course.prof_average = None
            
        rating_count += num_ratings

    return simple_courses

async def search_courses(search_params: AdvancedSearchParameters) -> Tuple[List[SimpleCourse], List[List[DetailedSection]]]:
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
        
    detailed_courses = add_gpa_data(detailed_courses)
    simple_courses = await add_prof_ratings(simple_courses)


    return detailed_courses, [course.sections for course in detailed_courses]

def parse_simple_course(course: ElementTree.Element) -> SimpleCourse:
    return SimpleCourse(
        id=course.get("id"),
        label=course.find("label").text,
        description=course.find("description").text if course.find("description") is not None else None,
        creditHours=course.find("creditHours").text,
        href=course.get("href")
    )

def parse_detailed_section(detailed_section: ElementTree.Element) -> DetailedSection:
    section = DetailedSection(
        id=detailed_section.get("id"),
        sectionNumber=detailed_section.find("sectionNumber").text if detailed_section.find("sectionNumber") is not None else None,
        statusCode=detailed_section.find("statusCode").text,
        partOfTerm=detailed_section.find("partOfTerm").text if detailed_section.find("partOfTerm") is not None else None,
        sectionStatusCode=detailed_section.find("sectionStatusCode").text,
        enrollmentStatus=detailed_section.find("enrollmentStatus").text,
        startDate=detailed_section.find("startDate").text if detailed_section.find("startDate") is not None else None,
        endDate=detailed_section.find("endDate").text if detailed_section.find("endDate") is not None else None,
        meetings=[]
    )
    for meeting in detailed_section.findall(".//meeting"):
        section.meetings.append(parse_meeting(meeting))
    return section

def parse_meeting(meeting: ElementTree.Element) -> Meeting:
    meeting_obj = Meeting(
        type={"code": meeting.find("type").attrib.get("code"), "desc": meeting.find("type").attrib.get("desc")},
        start=meeting.find("start").text,
        end=meeting.find("end").text if meeting.find("end") is not None else None,
        daysOfTheWeek=meeting.find("daysOfTheWeek").text if meeting.find("daysOfTheWeek") is not None else None,
        roomNumber=meeting.find("roomNumber").text if meeting.find("roomNumber") is not None else None,
        buildingName=meeting.find("buildingName").text if meeting.find("buildingName") is not None else None,
        instructors=[]
    )
    for instructor in meeting.findall(".//instructor"):
        meeting_obj.instructors.append(parse_instructor(instructor))
    return meeting_obj


def parse_instructor(instructor: ElementTree.Element) -> Instructor:
    return Instructor(
        lastName=instructor.get("lastName"),
        firstName=instructor.get("firstName")
    )
    
def filter_courses_by_id(simple_courses: List[SimpleCourse], course_id: str) -> List[SimpleCourse]:
    return [course for course in simple_courses if str(course_id) in course.id]

def filter_sections_by_id(simple_courses: List[SimpleCourse], simple_courses_filtered: List[SimpleCourse],  detailed_sections: List[DetailedSection], course_id: str) -> List[DetailedSection]:
    return  [detailed_sections for course, detailed_sections in zip(simple_courses, detailed_sections) if course.id in [sc.id for sc in simple_courses_filtered]]

def filter_courses_by_level(simple_courses: List[SimpleCourse], course_level: str) -> List[SimpleCourse]:
    return [course for course in simple_courses if course.id.split(" ")[1][0] == course_level]

def filter_sections_by_level(simple_courses: List[SimpleCourse], simple_courses_filtered: List[SimpleCourse], detailed_sections_list: List[List[DetailedSection]], course_level: str) -> List[List[DetailedSection]]:
    return [detailed_sections for course, detailed_sections in zip(simple_courses, detailed_sections_list) if course.id in [sc.id for sc in simple_courses_filtered]]

def average_gpa_by_course(gpa_dataframe: pl.DataFrame, subject: str, number: int) -> pl.DataFrame:
    gpa_dataframe = gpa_dataframe.groupby(["Subject", "Number"]).agg(pl.col("GPA").mean().alias("Average_GPA"))
    course_average_gpa = gpa_dataframe.filter((gpa_dataframe["Subject"] == subject) & (gpa_dataframe["Number"] == number)).select("Average_GPA")
    if course_average_gpa.height > 0:
        average_gpa_value = course_average_gpa["Average_GPA"].to_list()[0]
        return average_gpa_value
    else:
        return None

def add_gpa_data(simple_courses: List[SimpleCourse]) -> List[SimpleCourse]:
    for course in simple_courses:
        subj, num = course.id.split(" ")
        course.gpa_average = average_gpa_by_course(gpa_dataframe, subj, num)
    return simple_courses

# TODO: add code for filtering by on campus classes
# TODO: add communication in the frontend explaining that some fields don't qualify as fields that substantiate a search
# TODO: add code to filter for open sections
# TODO: add code for match_all/match_any geneds
def main():
    search_params = AdvancedSearchParameters(
        year="2023",
        term="spring",
        # course_id="340",
        # online=False,
        subject="CS",
        # college="KV",
        # credit_hours="3",
        # part_of_term="A",
        # gened_reqs=["HUM"],
        # course_level="2",
        # keyword_type="qs",
        # keyword="ethical"
        # instructor="fagen-ulmschneider"
    )
    simple_courses, detailed_sections_list = asyncio.run(search_courses(search_params))
    print(time_spent_getting_profs)
    print(time_spent_getting_ratings)
    print(rating_count)
    for i in range(len(simple_courses)):
        print(f"Course: {simple_courses[i].id} - {simple_courses[i].label}")
        print(f"    Average GPA: {simple_courses[i].gpa_average}")
        print(f"    Average PROF: {simple_courses[i].prof_average}")
        # for section in simple_courses[i].sections:
        #     print(f"    Section: {section.sectionNumber} - {section.statusCode} - {section.partOfTerm} - {section.sectionStatusCode} - {section.enrollmentStatus} - {section.startDate} - {section.endDate}")
        #     for meeting in section.meetings:
        #         print(f"        Meeting: {meeting.type} - {meeting.start} - {meeting.end} - {meeting.daysOfTheWeek} - {meeting.roomNumber} - {meeting.buildingName}")
        #         for instructor in meeting.instructors:
        #             print(f"            Instructor: {instructor.lastName} - {instructor.firstName}")
    
if __name__ == "__main__":
    main()
