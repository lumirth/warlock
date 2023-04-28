from .courses import search_courses, get_single_course_xml
from .datautils import load_gpa_data, initialize_professor_cache, save_professor_cache
from .models import Course, Parameters
from .models import parse_string_into_parameters, load_pickles
from .utils import logger, log_entry_exit
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import asyncio
import time

PROFESSOR_CACHE = {}
GPA_DATAFRAME = None
PICKLES = None
app = FastAPI()

# Middleware for allowing CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add the startup event
@app.on_event("startup")
async def startup_event():
    global PROFESSOR_CACHE
    global GPA_DATAFRAME
    global PICKLES
    
    PROFESSOR_CACHE = await initialize_professor_cache('data')
    if PROFESSOR_CACHE is None:
        raise RuntimeError("Failed to load professor cache")

    GPA_DATAFRAME = load_gpa_data(feather_file='data/gpa/gpa.feather')
    if GPA_DATAFRAME is None:
        raise RuntimeError("Failed to load GPA data")

    PICKLES = load_pickles("data")
    if PICKLES is None:
        raise RuntimeError("Failed to load pickles")

@app.get("/")
def read_root():
    return {"msg": "Hello, World!"}

@app.get("/search/simple", response_model=List[Course])
def search_simple(query: str):
    print('Searching for query:', query)
    if PROFESSOR_CACHE is {} or GPA_DATAFRAME is None or PICKLES is None:
        print('Waiting for data to load')
        time.sleep(10)
    query_obj = parse_string_into_parameters(query, PICKLES)
    results = search_advanced(query_obj)
    print('Got results in simple')
    print(len(results))
    for result in results:
        print(result)
    return results

@app.post("/search/advanced", response_model=List[Course])
def search_advanced(params: Parameters):
    print('Sending search request for params')
    if PROFESSOR_CACHE is {} or GPA_DATAFRAME is None or PICKLES is None:
        print('Waiting for data to load')
        time.sleep(10)
    results = asyncio.run(search_courses(params, professor_cache=PROFESSOR_CACHE, gpa_data=GPA_DATAFRAME))
    print('Got results')
    return results

@app.post("/course/sections", response_model=Course)
def get_course_sections(course: Course):
    Parameters = Parameters(
        year=course.year,
        term=course.term,
        subject=course.id.split(' ')[0],
        course_id=course.id
    )
    xml = asyncio.run(get_single_course_xml(Parameters))