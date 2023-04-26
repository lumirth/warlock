from . import rmp
from .gpa import gpa_dataframe
from .models import SimpleCourse
from typing import List
import asyncio
import os
import pickle
import polars as pl
import threading

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

LOAD_PICKLES = True
PICKLES_DIR = "../pickles"

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

# # A function to refresh the cache
# def refresh_cache():
#     while True:
#         PROFESSOR_CACHE.clear()
#         asyncio.run(rmp.fetch_all_professors())
#         print("Professor cache refreshed.")
#         # Wait for 6 hours before refreshing again
#         time.sleep(6 * 60 * 60)

# # Start the refresh_cache thread
# cache_refresh_thread = threading.Thread(target=refresh_cache)
# cache_refresh_thread.start()


def get_list_of_instructors(simple_course: SimpleCourse) -> List[str]:
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

def add_gpa_data(simple_courses: List[SimpleCourse]) -> List[SimpleCourse]:
    for course in simple_courses:
        subj, num = course.id.split(" ")
        course.gpa_average = average_gpa_by_course(gpa_dataframe, subj, num)
    return simple_courses

# TODO: add note to frontend that explains that professor matching is by last name, first initial only.
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
