from ..models import Course, Section, Parameters, Meeting, Instructor
import aiohttp
import xml.etree.ElementTree as ElementTree

# TODO: Add code that gets the GenEd attributes for a course

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