from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import api.courses as courses
from .models import SimpleCourse, DetailedCourse, AdvancedSearchParameters

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
    search_results = courses.search_simple(query)
    return search_results

@app.post("/search/advanced", response_model=List[SimpleCourse])
def search_advanced(advanced_search: AdvancedSearchParameters):
    search_results = courses.search_advanced(advanced_search)
    return search_results

@app.get("/course/{year}/{term}/{subj}/{id}", response_model=DetailedCourse)
def get_course(year: int, term: int, subj: str, id: int):
    course = courses.get_course(year, term, subj, id)
    if course:
        return course
    else:
        raise HTTPException(status_code=404, detail="Course not found")
