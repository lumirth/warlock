from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import api.search as searching
from api.courses import SimpleCourse, AdvancedSearchParameters, DetailedSection
from api.courses import initialize_professor_cache, save_professor_cache
from api.courses import load_gpa_data

PROFESSOR_CACHE = None
GPA_DATA = None

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def publish_message():
    global PROFESSOR_CACHE
    global GPA_DATA
    PROFESSOR_CACHE = initialize_professor_cache()
    GPA_DATA = load_gpa_data()
    print('Loaded data')

@app.get("/")
def read_root():
    return {"msg": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/search/simple", response_model=List[SimpleCourse])
def search_simple(query: str):
    print('Received query: ' + query)
    search_results = searching.search_simple(query, PROFESSOR_CACHE, GPA_DATA)
    return search_results

@app.post("/search/advanced", response_model=List[SimpleCourse])
def search_advanced(advanced_search: AdvancedSearchParameters):
    search_results = searching.search_advanced(advanced_search)
    return search_results

@app.get("/course/{year}/{term}/{subj}/{id}", response_model=SimpleCourse)
def get_course(year: int, term: int, subj: str, id: int):
    course = searching.get_course(year, term, subj, id)
    if course:
        return course
    else:
        raise HTTPException(status_code=404, detail="Course not found")
    
# endpoint for loading reddit API data on a detailed course page
@app.get("/course/{year}/{term}/{subj}/{id}/reddit", response_model=List[DetailedSection])
def get_reddit_data(year: int, term: int, subj: str, id: int):
    # undfined for now
    return

# endpoitn for loading detailed GPA graphs on a detailed course page    
@app.get("/course/{year}/{term}/{subj}/{id}/gpa", response_model=List[DetailedSection])
def get_gpa_data(year: int, term: int, subj: str, id: int):
    # undefined for now
    return

