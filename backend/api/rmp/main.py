import asyncio
import aiohttp
if __name__ != "__main__":
    from .constants import AUTH_TOKEN
    from .queries import autocomplete_school_query, search_teacher_query, get_teacher_query
else:
    from constants import AUTH_TOKEN
    from queries import autocomplete_school_query, search_teacher_query, get_teacher_query

UNIVERSITY_ID = "U2Nob29sLTExMTI="
API_URL = "https://www.ratemyprofessors.com/graphql"
HEADERS = {
    "authorization": f"Basic {AUTH_TOKEN}",
}

async def search_teacher(session, name, school_id=UNIVERSITY_ID):
    response = await session.post(
        API_URL,
        json={
            "query": search_teacher_query,
            "variables": {
                "text": name,
                "schoolID": school_id
            }
        },
        headers=HEADERS
    )
    result = await response.json(content_type=None)
    if result['data']['newSearch']['teachers'] is None:
        return []
    return [edge['node'] for edge in result['data']['newSearch']['teachers']['edges']]

async def get_teacher(session, teacher_id):
    response = await session.post(
        API_URL,
        json={
            "query": get_teacher_query,
            "variables": {
                "id": teacher_id
            }
        },
        headers=HEADERS
    )
    result = await response.json(content_type=None)
    return result['data']['node']

async def get_teacher_info(session, name, school_id):
    teachers = await search_teacher(session, name, school_id)
    if not teachers:
        return None
    teacher_id = teachers[0]['id']
    teacher = await get_teacher(session, teacher_id)
    return teacher

async def get_ratings_for_teachers(instructors, school_id=UNIVERSITY_ID):
    # print("-- Getting ratings for {} instructors ---".format(len(instructors)))
    async with aiohttp.ClientSession() as session:
        tasks = [get_teacher_info(session, instructor, school_id) for instructor in instructors]
        results = await asyncio.gather(*tasks)
    # print("--- Done getting ratings for instructors ---")
    return results

import time
if __name__ == "__main__":
    instructors = ["Woodley", "Wade"] 
    # append instructors to itself  2000 times
    instructors = instructors * 2000
    school_id = "U2Nob29sLTExMTI="

    start = time.time()
    teachers_info = asyncio.run(get_ratings_for_teachers(instructors, school_id))
    end = time.time()
    print("Time taken: {}".format(end - start))
    # print(teachers_info)
