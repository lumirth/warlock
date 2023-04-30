from ..models import Course
from typing import List


def filter_courses_by_id(simple_courses: List[Course], course_id: str) -> List[Course]:
    filtered_courses = []
    for course in simple_courses:
        if course_id in course.id:
            filtered_courses.append(course)
    return filtered_courses


def filter_courses_by_level(simple_courses: List[Course], course_level: str) -> List[Course]:
    filtered_courses = []
    for course in simple_courses:
        if course.id.split(" ")[1][0] == course_level:
            filtered_courses.append(course)
    return filtered_courses