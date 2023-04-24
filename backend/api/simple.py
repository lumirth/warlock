import requests
from typing import List, Tuple
from xml.etree import ElementTree
from concurrent.futures import ThreadPoolExecutor
from models import SimpleCourse, DetailedSection, AdvancedSearchParameters, Instructor, Meeting

def prepare_query_params(search_params: AdvancedSearchParameters) -> dict:
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

def get_course_xml(query_params: dict) -> ElementTree.Element:
    base_url = "https://courses.illinois.edu/cisapp/explorer/schedule"
    courses_endpoint = f"{base_url}/courses.xml"
    response = requests.get(courses_endpoint, params=query_params)
    print(response.url)
    response.raise_for_status()
    return ElementTree.fromstring(response.content)

def parse_simple_course(course: ElementTree.Element) -> SimpleCourse:
    return SimpleCourse(
        id=course.get("id"),
        label=course.find("label").text,
        description=course.find("description").text,
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

def get_course_details(simple_course: SimpleCourse) -> List[DetailedSection]:
    response = requests.get(simple_course.href, params={"mode": "cascade"})
    response.raise_for_status()
    course_xml_data = ElementTree.fromstring(response.content)
    return [parse_detailed_section(detailed_section) for detailed_section in course_xml_data.findall(".//detailedSection")]

def filter_courses_by_id(simple_courses: List[SimpleCourse], course_id: str) -> List[SimpleCourse]:
    return [course for course in simple_courses if str(course_id) in course.id]

def filter_sections_by_id(simple_courses: List[SimpleCourse], simple_courses_filtered: List[SimpleCourse],  detailed_sections: List[DetailedSection], course_id: str) -> List[DetailedSection]:
    return  [detailed_sections for course, detailed_sections in zip(simple_courses, detailed_sections) if course.id in [sc.id for sc in simple_courses_filtered]]

def filter_courses_by_level(simple_courses: List[SimpleCourse], course_level: str) -> List[SimpleCourse]:
    return [course for course in simple_courses if course.id.split(" ")[1][0] == course_level]

def filter_sections_by_level(simple_courses: List[SimpleCourse], simple_courses_filtered: List[SimpleCourse], detailed_sections_list: List[List[DetailedSection]], course_level: str) -> List[List[DetailedSection]]:
    return [detailed_sections for course, detailed_sections in zip(simple_courses, detailed_sections_list) if course.id in [sc.id for sc in simple_courses_filtered]]

def search_courses(search_params: AdvancedSearchParameters) -> Tuple[List[SimpleCourse], List[List[DetailedSection]]]:
    query_params = prepare_query_params(search_params)
    course_xml = get_course_xml(query_params)

    with ThreadPoolExecutor() as executor:
        simple_courses = list(map(parse_simple_course, course_xml.findall(".//course")))
        detailed_sections_list = list(executor.map(get_course_details, simple_courses))

    if search_params.course_id is not None:
        simple_courses_filtered = filter_courses_by_id(simple_courses, search_params.course_id)
        detailed_sections_filtered = filter_sections_by_id(simple_courses, simple_courses_filtered, detailed_sections_list, search_params.course_id)
        simple_courses = simple_courses_filtered
        detailed_sections_list = detailed_sections_filtered
        
    if search_params.course_level is not None:
        simple_courses_filtered = filter_courses_by_level(simple_courses, search_params.course_level)
        detailed_sections_filtered = filter_sections_by_level(simple_courses, simple_courses_filtered, detailed_sections_list, search_params.course_level)
        simple_courses = simple_courses_filtered
        detailed_sections_list = detailed_sections_filtered

    return simple_courses, detailed_sections_list


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
        # subject="CS",
        # college="KV",
        # credit_hours="3",
        part_of_term="A",
        gened_reqs=["HUM"],
        # course_level="2",
        # keyword_type="qs",
        # keyword="ethical"
        # instructor="fagen-ulmschneider"
    )
    simple_courses, detailed_sections_list = search_courses(search_params)
    for i in range(len(simple_courses)):
        print(f"Course: {simple_courses[i].id} - {simple_courses[i].label}")
        for section in detailed_sections_list[i]:
            print(f"    Section: {section.sectionNumber} - {section.statusCode} - {section.partOfTerm} - {section.sectionStatusCode} - {section.enrollmentStatus} - {section.startDate} - {section.endDate}")
            for meeting in section.meetings:
                print(f"        Meeting: {meeting.type} - {meeting.start} - {meeting.end} - {meeting.daysOfTheWeek} - {meeting.roomNumber} - {meeting.buildingName}")
                for instructor in meeting.instructors:
                    print(f"            Instructor: {instructor.lastName} - {instructor.firstName}")
    
if __name__ == "__main__":
    main()
