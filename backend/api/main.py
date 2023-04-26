from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import api.search as searching
from api.courses.models import SimpleCourse, DetailedSection, AdvancedSearchParameters

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"msg": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get("/search/simple", response_model=List[SimpleCourse])
def search_simple(query: str):
    # search_results = courses.search_simple(query)
    # return search_results
    simple = SimpleCourse(id="cs 110")
    return [simple]

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

