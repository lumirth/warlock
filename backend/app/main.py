from .courses import search_courses
from .datautils import load_gpa_data, initialize_professor_cache, save_professor_cache
from .models import Course, Parameters
from .models import parse_string_into_parameters, load_pickles
from .utils import logger, log_entry_exit
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import asyncio

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
    query_obj = parse_string_into_parameters(query, PICKLES)
    results = search_advanced(query_obj)
    for result in results:
        print(result)
    return results

@app.post("/search/advanced", response_model=List[Course])
def search_advanced(params: Parameters):
    results = asyncio.run(search_courses(params, professor_cache=PROFESSOR_CACHE, gpa_data=GPA_DATAFRAME))
    return results
