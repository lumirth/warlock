from ..models import Course, GenEd
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


def meeting_type_code_is_online(type_code: str):
    return type_code[0] == "O" or type_code[0] == "E"


def filter_courses_by_online_or_campus(full_courses: List[Course], flag: str = "both") -> List[Course]:
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
            print(course.id)
            print(gened_ids_set, course_gened_ids_set)
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

def filter_courses_by_instructor_last_name(courses: List[Course], last_name: str) -> List[Course]:
    filtered_courses = []
    for course in courses:
        for section in course.sections:
            for meeting in section.meetings:
                for instructor in meeting.instructors:
                    if instructor.lastName.lower() == last_name.lower():
                        filtered_courses.append(course)
                        break
    return filtered_courses

def filter_courses_by_keyword(courses: List[Course], keyword: str, keyword_type: str) -> List[Course]:
    filtered_courses = []
    
    # Helper function to check if text contains all/any of the words in the keyword_list
    def check_words(text, keyword_list, search_type):
        if search_type == "all":
            return all(word in text.lower() for word in keyword_list)
        elif search_type == "any":
            return any(word in text.lower() for word in keyword_list)
    
    # Prepare the keyword list based on keyword_type
    if keyword_type == "qs":
        keyword_list = [keyword.lower()]
        search_type = "any"
    elif keyword_type == "qp":
        keyword_list = [keyword.lower().replace("+", " ")]
        search_type = "any"
    elif keyword_type == "qw_a":
        keyword_list = keyword.lower().split(" ")
        search_type = "all"
    elif keyword_type == "qw_o":
        keyword_list = keyword.lower().split(" ")
        search_type = "any"
    else:
        raise ValueError("Invalid keyword_type")

    for course in courses:
        title_desc = course.label + " " + course.description
        course_section_info = course.courseSectionInformation if course.courseSectionInformation else ""
        section_degree_attr = course.sectionDegreeAttributes if course.sectionDegreeAttributes else ""
        
        if check_words(title_desc, keyword_list, search_type) or \
           check_words(course_section_info, keyword_list, search_type) or \
           check_words(section_degree_attr, keyword_list, search_type):
            filtered_courses.append(course)
            
    return filtered_courses
