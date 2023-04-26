from typing import List, Tuple
from xml.etree import ElementTree
from models import SimpleCourse, DetailedSection, AdvancedSearchParameters, Instructor, Meeting
import polars as pl
from data_loader import gpa_dataframe
import asyncio
import aiohttp
import rmp
import time
import pickle
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

LOAD_PICKLES = True
PICKLES_DIR = "pickles"

print("Initializing professor cache...")
if LOAD_PICKLES:
    # load professor cache from pickle file
    PROFESSOR_CACHE = pickle.load(open(os.path.join(PICKLES_DIR, "professor_cache.pkl"), "rb"))
    print("Professor cache loaded.")
else:
    # Initialize the professor cache
    PROFESSOR_CACHE = asyncio.run(rmp.fetch_all_professors())
    print("Professor cache initialized.")

print("Saving professor cache...")
PICKLES_DIR = "pickles"
# save professor cache to pickle file
if not os.path.exists(PICKLES_DIR):
    os.makedirs(PICKLES_DIR)
pickle.dump(PROFESSOR_CACHE, open(os.path.join(PICKLES_DIR, "professor_cache.pkl"), "wb"))
print("Professor cache saved.")


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


def get_list_of_instructors(simple_course: SimpleCourse) -> List[str]:
    instructors = set()
    for section in simple_course.sections:
        for meeting in section.meetings:
            for instructor in meeting.instructors:
                instructors.add(f"{instructor.firstName} {instructor.lastName}")
    return list(instructors)


def get_professor_data_from_cache(instructor_name: str) -> dict:
    return PROFESSOR_CACHE.get(instructor_name)


async def add_prof_ratings(simple_courses: List[SimpleCourse]) -> List[SimpleCourse]:
    for course in simple_courses:
        instructor_names = get_list_of_instructors(course)
        instructor_data = [get_professor_data_from_cache(name) for name in instructor_names]

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

    flag = "both"
    if search_params.online:
        flag = "online"
    if search_params.on_campus:
        flag = "campus"
    if search_params.online and search_params.on_campus:
        flag = "both"

    detailed_courses = filter_courses_by_online_or_campus(detailed_courses, flag=flag)

    detailed_courses = add_gpa_data(detailed_courses)
    simple_courses = await add_prof_ratings(simple_courses)

    return detailed_courses


def parse_simple_course(course: ElementTree.Element) -> SimpleCourse:
    parents = course.find("parents")
    return SimpleCourse(
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


def filter_courses_by_id(simple_courses: List[SimpleCourse], course_id: str) -> List[SimpleCourse]:
    """Filters a list of SimpleCourse objects by a given course ID.

    Args:
        simple_courses: A list of SimpleCourse objects to filter.
        course_id: A string representing the course ID to filter by.

    Returns:
        A list of SimpleCourse objects with IDs containing the specified course_id.
    """
    filtered_courses = []
    for course in simple_courses:
        if course_id in course.id:
            filtered_courses.append(course)
    return filtered_courses


def filter_courses_by_level(simple_courses: List[SimpleCourse], course_level: str) -> List[SimpleCourse]:
    """Filters a list of SimpleCourse objects by a given course level.

    Args:
        simple_courses: A list of SimpleCourse objects to filter.
        course_level: A string representing the course level to filter by.

    Returns:
        A list of SimpleCourse objects with IDs containing the specified course_level.
    """
    filtered_courses = []
    for course in simple_courses:
        if course.id.split(" ")[1][0] == course_level:
            filtered_courses.append(course)
    return filtered_courses


def meeting_type_code_is_online(type_code: str):
    """Returns True if the meeting type code is online or electronic

    Args:
        type_code (str): The meeting type code

    Returns:
        bool: True if the meeting type code is online or electronic
    """
    return type_code[0] == "O" or type_code[0] == "E"


def filter_courses_by_online_or_campus(full_courses: List[SimpleCourse], flag: str = "both") -> List[SimpleCourse]:
    """Returns a list of courses that have online or on campus sections depending on the flag

    Args:
        courses (List[SimpleCourse]): List of courses to filter
        flag (bool): True if online, False if on campus (default True)

    Returns:
        List[SimpleCourse]: List of courses that have online or on campus sections depending on the flag
    """
    if flag == "both":
        return full_courses
    elif flag == "online":
        want_online = True
    elif flag == "campus":
        want_online = False
    courses = []
    for course in full_courses:
        keep_course = False
        for section in course.sections:
            for meeting in section.meetings:
                if want_online and meeting_type_code_is_online(meeting.typeCode):
                    keep_course = True
                if not want_online and not meeting_type_code_is_online(meeting.typeCode):
                    keep_course = True
        if keep_course:
            courses.append(course)
    return courses


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


# TODO: add code for match_all/match_any geneds
# - this will require filtering courses by their gen ed requirements
# TODO: rework logic to visit the individual course API page and get gened reqs from there because schedule/courses API doesn't have gened reqs
def main():
    # TODO: write tests for this
    search_params = AdvancedSearchParameters(
        year="2023",
        term="spring",
        # course_id="340",
        # online=True,
        # on_campus=True,
        subject="PHIL",
        # college="KV",
        # credit_hours="3",
        # part_of_term="A",
        # gened_reqs=["HUM"],
        # course_level="2",
        keyword_type="qs",
        keyword="minds"
        # instructor="woodley"
    )

    import textwrap
    import shutil

    def print_with_indent(text, indent=4, width=70):
        terminal_width = shutil.get_terminal_size().columns
        width = terminal_width - indent
        # Create a TextWrapper object with the specified indentation and width
        wrapper = textwrap.TextWrapper(initial_indent=" " * indent, subsequent_indent=" " * indent, width=width)

        # remove all newlines from the text
        text = text.replace("\n", " ")
        # Use the TextWrapper object to wrap the text
        wrapped_text = wrapper.fill(text)

        # Print the wrapped text
        print(wrapped_text)

    def load_courses():
        simple_courses = asyncio.run(search_courses(search_params))
        return simple_courses

    def print_courses(simple_courses):
        for i in range(len(simple_courses)):
            print(f"{simple_courses[i].id} - {simple_courses[i].label}") if simple_courses[i].label is not None else None
            print_with_indent(f"Year: {simple_courses[i].year}") if simple_courses[i].year is not None else None
            print_with_indent(f"Term: {simple_courses[i].term}") if simple_courses[i].term is not None else None
            print_with_indent(f"Subject: {simple_courses[i].subject}") if simple_courses[i].subject is not None else None
            print_with_indent(f"Description: {simple_courses[i].description}") if simple_courses[i].description is not None else None
            print_with_indent(f"Credit Hours: {simple_courses[i].creditHours}") if simple_courses[i].creditHours is not None else None
            print_with_indent(f"Attributes: {simple_courses[i].sectionDegreeAttributes}") if simple_courses[i].sectionDegreeAttributes is not None else None
            # print_with_indent(f"Section Info: {simple_courses[i].courseSectionInformation}") if simple_courses[i].courseSectionInformation is not None else None
            print_with_indent(f"GPA : {simple_courses[i].gpa_average}") if simple_courses[i].gpa_average is not None else None
            print_with_indent(f"PROF: {simple_courses[i].prof_average}") if simple_courses[i].prof_average is not None else None

            for section in simple_courses[i].sections:
                if section.enrollmentStatus != "UNKNOWN":
                    print_with_indent(f"Section: {section.sectionNumber} - POT {section.partOfTerm} - {section.enrollmentStatus} - {section.startDate} - {section.endDate}", indent=8)
                else:
                    print_with_indent(f"Section: {section.sectionNumber} - POT {section.partOfTerm} - {section.startDate} - {section.endDate}", indent=8)
                for meeting in section.meetings:
                    days = meeting.daysOfTheWeek.strip() if meeting.daysOfTheWeek is not None else None
                    print_with_indent(f"Meeting: {meeting.typeCode} - {meeting.start} - {meeting.end} - {days} - {meeting.roomNumber} - {meeting.buildingName}", indent=12)
                    for instructor in meeting.instructors:
                        print_with_indent(f"Instructor: {instructor.lastName}, {instructor.firstName}", indent=16)

    s = load_courses()
    print_courses(s)

    def update_type_codes(courses, type_codes):
        # Loop through courses and extract type codes and descriptions
        for course in courses:
            for section in course.sections:
                for meeting in section.meetings:
                    type_codes[meeting.typeCode] = meeting.typeDesc

        # Return the updated dictionary of type codes
        return type_codes

    department_codes = [
        "ACCY",
        "ASRM",
        "ADV",
        "AE",
        "AFRO",
        "AFST",
        "AGCM",
        "AGED",
        "ALEC",
        "ABE",
        "ACE",
        "ACES",
        "AFAS",
        "AIS",
        "ANSC",
        "ANTH",
        "AHS",
        "ALS",
        "ARAB",
        "ARCH",
        "ART",
        "ARTD",
        "ARTE",
        "ARTF",
        "ARTH",
        "ARTS",
        "AAS",
        "ASST",
        "ASTR",
        "ATMS",
        "AVI",
        "BMNA",
        "BASQ",
        "BIOC",
        "BIOE",
        "BIOL",
        "BSE",
        "BIOP",
        "BCS",
        "BCOG",
        "BR",
        "BULG",
        "BUS",
        "BADM",
        "BDI",
        "BTW",
        "CHP",
        "CATL",
        "CDB",
        "CSB",
        "CAS",
        "CHBE",
        "CHEM",
        "CHIN",
        "CINE",
        "CEE",
        "CLCV",
        "CLE",
        "CIC",
        "CMN",
        "CHLH",
        "CB",
        "CWL",
        "CSE",
        "CS",
        "CW",
        "CPSC",
        "CI",
        "CZCH",
        "DANC",
        "ESE",
        "EALC",
        "ECON",
        "EDUC",
        "EPOL",
        "ERAM",
        "EOL",
        "EPS",
        "EDPR",
        "EPSY",
        "ECE",
        "ENG",
        "ENGH",
        "ETMA",
        "ENGL",
        "ESL",
        "EIL",
        "ENT",
        "ENVS",
        "ENSU",
        "EURO",
        "FIN",
        "FAA",
        "FSHN",
        "FLTE",
        "FR",
        "GSD",
        "GWS",
        "GE",
        "GS",
        "GEOG",
        "GGIS",
        "GEOL",
        "GER",
        "GMC",
        "GLBL",
        "GC",
        "GCL",
        "GRK",
        "HT",
        "HEBR",
        "HNDI",
        "HIST",
        "HORT",
        "HDFS",
        "HDES",
        "HRD",
        "HRE",
        "HCD",
        "DTX",
        "HUM",
        "IE",
        "INFO",
        "IS",
        "IB",
        "IHLT",
        "ITAL",
        "ARTJ",
        "JAPN",
        "JS",
        "JOUR",
        "KIN",
        "KOR",
        "LER",
        "LIR",
        "LA",
        "LAT",
        "LAST",
        "LLS",
        "LAW",
        "LCTL",
        "LAS",
        "LIS",
        "LGLA",
        "LING",
        "SLCL",
        "MFGE",
        "MSE",
        "MATH",
        "ME",
        "MDIA",
        "MS",
        "MACS",
        "MDVL",
        "MFST",
        "MICR",
        "MILS",
        "GRKM",
        "MCB",
        "MIP",
        "MUSE",
        "MUS",
        "MUSC",
        "NRES",
        "NS",
        "NE",
        "NEUR",
        "NPRE",
        "NUTR",
        "LEAD",
        "PATH",
        "PERS",
        "PHIL",
        "PHYS",
        "PBIO",
        "PLPA",
        "POL",
        "PS",
        "PORT",
        "PSM",
        "PSYC",
        "QUEC",
        "RST",
        "MBA",
        "REHB",
        "REL",
        "RLST",
        "RHET",
        "RMLG",
        "RSOC",
        "RUSS",
        "REES",
        "SNSK",
        "SCAN",
        "SLS",
        "SCR",
        "SLAV",
        "SOCW",
        "SOC",
        "SAME",
        "SPAN",
        "SPED",
        "SPCM",
        "SHS",
        "STAT",
        "SBC",
        "SWAH",
        "SE",
        "TSM",
        "TE",
        "TMGT",
        "THEA",
        "TAM",
        "TRST",
        "TURK",
        "UKR",
        "UP",
        "VB",
        "VCM",
        "VM",
        "WLOF",
        "WGGP",
        "WRIT",
        "YDSH",
        "COMM",
        "ESES",
        "LEIS",
        "VP",
        "ZULU",
    ]

    # search_params.year="2020"
    # type_codes = dict()
    # for code in department_codes:
    #     search_params.subject = code
    #     s = load_courses()
    #     type_codes = update_type_codes(s, type_codes)
    # import pprint
    # pprint.pprint(type_codes)


if __name__ == "__main__":
    main()
