from ..models import Course, GenEd
from typing import List


def filter_courses_by_id(simple_courses: List[Course], course_id: str) -> List[Course]:
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


def filter_courses_by_level(simple_courses: List[Course], course_level: str) -> List[Course]:
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


def filter_courses_by_online_or_campus(full_courses: List[Course], flag: str = "both") -> List[Course]:
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


def filter_courses_by_gen_eds(courses: List[Course], gened_ids: List[str], match_any: bool=False):
    if match_any:
        return filter_courses_by_any_gen_eds(courses, gened_ids)
    else:
        return filter_courses_by_all_gen_eds(courses, gened_ids)
    
def filter_courses_by_any_gen_eds(courses: List[Course], gened_ids: List[str]) -> List[Course]:
    filtered_courses = []
    for course in courses:
        if course.genEdAttributes is not None:
            for gened in course.genEdAttributes:
                if gened.id in gened_ids:
                    filtered_courses.append(course)
                    break
    return filtered_courses

def filter_courses_by_all_gen_eds(courses: List[Course], gened_ids: List[str]) -> List[Course]:
    filtered_courses = []
    for course in courses:
        if course.genEdAttributes is not None:
            gened_ids_set = set(gened_ids)
            course_gened_ids_set = set([gened.id for gened in course.genEdAttributes])

            if gened_ids_set.issubset(course_gened_ids_set):
                filtered_courses.append(course)
    return filtered_courses

def filter_courses_by_credit_hours(courses: List[Course], credit_hours: int) -> List[Course]:
    filtered_courses = []
    for course in courses:
        if course.creditHours is not None:
                if course.creditHours == credit_hours:
                    filtered_courses.append(course)
    return filtered_courses

def filter_courses_by_part_of_term(courses: List[Course], part_of_term: str) -> List[Course]:
    # if any section has matching part of term, keep course
    filtered_courses = []
    for course in courses:
        for section in course.sections:
            if section.partOfTerm == part_of_term:
                filtered_courses.append(course)
                break
    return filtered_courses 