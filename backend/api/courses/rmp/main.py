import asyncio
import aiohttp
from aiohttp import TCPConnector
if __name__ != "__main__":
    from .constants import AUTH_TOKEN
    from .queries import combined_query
else:
    from constants import AUTH_TOKEN
    from queries import combined_query

UNIVERSITY_ID = "U2Nob29sLTExMTI="
API_URL = "https://www.ratemyprofessors.com/graphql"
HEADERS = {
    "authorization": f"Basic {AUTH_TOKEN}",
}

async def get_teacher_info(session, name, school_id):
    response = await session.post(
        API_URL,
        json={
            "query": combined_query,
            "variables": {
                "text": name,
                "schoolID": school_id
            }
        },
        headers=HEADERS
    )
    result = await response.json(content_type=None)
    teachers = result['data']['newSearch']['teachers']['edges']
    if not teachers:
        return None
    return teachers[0]['node']

async def get_ratings_for_teachers(instructors, school_id=UNIVERSITY_ID):
    conn = TCPConnector(limit=300)
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = [get_teacher_info(session, instructor, school_id) for instructor in instructors]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

import time
if __name__ == "__main__":
    instructors = ["Woodley", "Wade"]
    instructors = instructors * 2000
    school_id = "U2Nob29sLTExMTI="

    start = time.time()
    teachers_info = asyncio.run(get_ratings_for_teachers(instructors, school_id))
    end = time.time()
    print("Time taken: {}".format(end - start))
