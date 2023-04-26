from .models import SimpleCourse
from typing import List


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
