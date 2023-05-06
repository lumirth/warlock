from ..models import Course, Section, Parameters, Meeting, Instructor
import aiohttp
import xml.etree.ElementTree as ElementTree
from ..utils import logger

async def get_course_search_xml(query_params: dict) -> ElementTree.Element:
    base_url = "https://courses.illinois.edu/cisapp/explorer/schedule"
    courses_endpoint = f"{base_url}/courses.xml"
    async with aiohttp.ClientSession() as session:
        async with session.get(courses_endpoint, params=query_params) as response:
            logger.info("Getting course xml, URL:")
            logger.info(response.url)
            response.raise_for_status()
            content = await response.read()
    return ElementTree.fromstring(content)


async def get_section_xml_from_crn(search_params: Parameters) -> ElementTree.Element:
    base_url = "https://courses.illinois.edu/cisapp/explorer/schedule"
    courses_endpoint = f"{base_url}/sections.xml"
    params = {
        "year": search_params.year,
        "term": search_params.term,
        "crn": search_params.crn,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(courses_endpoint, params=params) as response:
            logger.info("Getting section xml from crn, URL:")
            logger.info(response.url)
            response.raise_for_status()
            content = await response.read()
    return ElementTree.fromstring(content)


async def get_single_course_xml(search_params: Parameters) -> ElementTree.Element:
    base_url = "https://courses.illinois.edu/cisapp/explorer/schedule"
    endpoint = "{base_url}/{year}/{term}/{subject}/{course_id}.xml?mode=cascade".format(
        base_url=base_url,
        year=search_params.year,
        term=search_params.term.lower(),
        subject=search_params.subject.upper(),
        course_id=search_params.course_id,
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint) as response:
            logger.info("Getting single course xml, URL:")
            logger.info(response.url)
            response.raise_for_status()
            content = await response.read()
    return ElementTree.fromstring(content)
