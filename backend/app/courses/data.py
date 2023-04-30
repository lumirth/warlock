from ..models import Course
from typing import List
import polars as pl
from ..utils import log_entry_exit

def get_list_of_instructors(simple_course: Course) -> List[str]:
    instructors = set()
    for section in simple_course.sections:
        for meeting in section.meetings:
            for instructor in meeting.instructors:
                instructors.add(f"{instructor.firstName} {instructor.lastName}")
    return list(instructors)

def average_gpa_by_course(gpa_dataframe: pl.DataFrame) -> pl.DataFrame:
    return gpa_dataframe.groupby(["Subject", "Number"]).agg(pl.col("GPA").mean().alias("Average_GPA"))

def add_gpa_data(simple_courses: List[Course], gpa_data) -> List[Course]:
    average_gpa_dataframe = average_gpa_by_course(gpa_data)
    for course in simple_courses:
        subj, num = course.id.split(" ")
        course_average_gpa = average_gpa_dataframe.filter((average_gpa_dataframe["Subject"] == subj) & (average_gpa_dataframe["Number"] == int(num))).select("Average_GPA")
        if course_average_gpa.height > 0:
            course.gpa_average = course_average_gpa["Average_GPA"].to_list()[0]
    return simple_courses

def get_professor_data_from_cache(professor_cache: dict, instructor_name: str) -> dict:
    return professor_cache.get(instructor_name)

async def add_prof_ratings(simple_courses: List[Course], professor_cache: dict) -> List[Course]:
    for course in simple_courses:
        instructor_names = get_list_of_instructors(course)
        instructor_data = [get_professor_data_from_cache(professor_cache, name) for name in instructor_names]

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
