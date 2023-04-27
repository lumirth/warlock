from ..models import Course
from typing import List
import polars as pl

def get_list_of_instructors(simple_course: Course) -> List[str]:
    instructors = set()
    for section in simple_course.sections:
        for meeting in section.meetings:
            for instructor in meeting.instructors:
                instructors.add(f"{instructor.firstName} {instructor.lastName}")
    return list(instructors)

def average_gpa_by_course(gpa_dataframe: pl.DataFrame, subject: str, number: int) -> pl.DataFrame:
    gpa_dataframe = gpa_dataframe.groupby(["Subject", "Number"]).agg(pl.col("GPA").mean().alias("Average_GPA"))
    course_average_gpa = gpa_dataframe.filter((gpa_dataframe["Subject"] == subject) & (gpa_dataframe["Number"] == number)).select("Average_GPA")
    if course_average_gpa.height > 0:
        average_gpa_value = course_average_gpa["Average_GPA"].to_list()[0]
        return average_gpa_value
    else:
        return None

def add_gpa_data(simple_courses: List[Course], gpa_data) -> List[Course]:
    for course in simple_courses:
        subj, num = course.id.split(" ")
        course.gpa_average = average_gpa_by_course(gpa_data, subj, num)
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
