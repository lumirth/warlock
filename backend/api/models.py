from typing import List, Optional
from pydantic import BaseModel
from xml.etree.ElementTree import Element

class Instructor(BaseModel):
    lastName: str
    firstName: str
    rate_my_professor_id: Optional[str]
    department: Optional[str]
    avg_rating: Optional[float]
    avg_difficulty: Optional[float]
    num_ratings: Optional[int]

class Meeting(BaseModel):
    type: dict
    start: Optional[str]
    end: Optional[str]
    daysOfTheWeek: Optional[str]
    roomNumber: Optional[str]
    buildingName: Optional[str]
    instructors: List[Instructor]

class DetailedSection(BaseModel):
    id: str
    sectionNumber: Optional[str]
    statusCode: Optional[str]
    partOfTerm: Optional[str]
    sectionStatusCode: Optional[str]
    enrollmentStatus: Optional[str]
    startDate: Optional[str]
    endDate: Optional[str]
    meetings: List[Meeting]

class Category(BaseModel):
    id: str
    description: Optional[str]
    genEdAttributes: Optional[dict]

class SimpleCourse(BaseModel):
    id: str
    label: Optional[str]
    description: Optional[str]
    creditHours: Optional[str]
    gpa_average: Optional[float]
    href: Optional[str]  # Add href attribute to store the link to detailed course data

    @classmethod
    def from_xml_element(cls, course_xml: Element) -> 'SimpleCourse':
        course_id = course_xml.attrib["id"]
        title = course_xml.find("label").text
        description = course_xml.find("description").text
        credit_hours = course_xml.find("creditHours").text
        href = course_xml.attrib["href"]

        return cls(id=course_id, label=title, description=description, creditHours=credit_hours, href=href)

class DetailedCourse(SimpleCourse):
    sectionDegreeAttributes: Optional[str]
    genEdCategories: List[Category]
    detailedSections: List[DetailedSection]

class AdvancedSearchParameters(BaseModel):
    keyword: Optional[str]
    keyword_type: Optional[str]
    instructor: Optional[str]
    college: Optional[str]
    subject: Optional[str]
    credit_hours: Optional[str]
    section_attributes: Optional[str]
    course_level: Optional[str]
    gened_reqs: Optional[List[str]]
    match_all_gened_reqs: Optional[bool]
    match_any_gened_reqs: Optional[bool]
    part_of_term: Optional[str]
    online: Optional[bool]
    on_campus: Optional[bool]
    open_sections: Optional[bool]
    evenings: Optional[bool]

class Query(BaseModel):
    simple_query: Optional[str]
    advanced_query: Optional[AdvancedSearchParameters]

class CourseSearchResponse(BaseModel):
    courses: List[SimpleCourse]
    query: Query
