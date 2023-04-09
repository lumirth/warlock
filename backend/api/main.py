from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.query_parser import WarlockQuery

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

if __name__ == '__main__':
    query = WarlockQuery('math 257, year:2021, semester:fall, is:online, is:open')
    print(query)