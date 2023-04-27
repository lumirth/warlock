from ..models import Course, Section, Parameters, Meeting, Instructor
import aiohttp
import xml.etree.ElementTree as ElementTree

async def get_course_xml(query_params: dict) -> ElementTree.Element:
    base_url = "https://courses.illinois.edu/cisapp/explorer/schedule"
    courses_endpoint = f"{base_url}/courses.xml"
    async with aiohttp.ClientSession() as session:
        async with session.get(courses_endpoint, params=query_params) as response:
            print(response.url)
            response.raise_for_status()
            content = await response.read()
    return ElementTree.fromstring(content)

async def get_course_details(simple_course: Course) -> Course:
    async with aiohttp.ClientSession() as session:
        async with session.get(simple_course.href, params={"mode": "cascade"}) as response:
            response.raise_for_status()
            content = await response.read()
    course_xml_data = ElementTree.fromstring(content)
    detailed_sections = [parse_detailed_section(detailed_section) for detailed_section in course_xml_data.findall(".//detailedSection")]
    simple_course.sections = detailed_sections
    return simple_course

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
