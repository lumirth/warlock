from typing import List, Optional
from pydantic import BaseModel
from xml.etree.ElementTree import Element


class Instructor(BaseModel):
    lastName: str
    firstName: str
    department: Optional[str]
    avg_rating: Optional[float]
    avg_difficulty: Optional[float]
    num_ratings: Optional[int]


class Meeting(BaseModel):
    typeCode: Optional[str]
    typeDesc: Optional[str]
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
    year: Optional[str]
    term: Optional[str]
    subject: Optional[str]
    id: Optional[str]
    label: Optional[str]
    description: Optional[str]
    creditHours: Optional[str]
    gpa_average: Optional[float]
    prof_average: Optional[float]
    href: Optional[str] 
    sections: Optional[List[DetailedSection]]
    sectionDegreeAttributes: Optional[str]
    courseSectionInformation: Optional[str]
    genEdCategories: Optional[List[Category]]

    @classmethod
    def from_xml_element(cls, course_xml: Element) -> "SimpleCourse":
        course_id = course_xml.attrib["id"]
        title = course_xml.find("label").text
        description = course_xml.find("description").text
        credit_hours = course_xml.find("creditHours").text
        href = course_xml.attrib["href"]

        return cls(
            id=course_id,
            label=title,
            description=description,
            creditHours=credit_hours,
            href=href,
        )

class AdvancedSearchParameters(BaseModel):
    year: Optional[int]  # required
    term: Optional[str]  # required
    keyword: Optional[str]  # substantive
    keyword_type: Optional[str]  # NOT substantive, but required if keyword is present
    instructor: Optional[str]  # substantive
    college: Optional[str]  # substantive
    subject: Optional[str]  # substantive
    course_id: Optional[int]  # NOT substantive
    crn: Optional[int]  # substantive, but disregards other parameters
    credit_hours: Optional[str]  # substantive
    # section_attributes: Optional[str] # substantive
    course_level: Optional[str]  # NOT substantive
    gened_reqs: Optional[List[str]]  # substantive
    match_all_gened_reqs: Optional[bool]  # NOT substantive
    # but this or match_any_gened_reqs is required if gened_reqs is present. This is the default
    match_any_gened_reqs: Optional[bool]  # NOT substantive
    # but this or match_all_gened_reqs is required if gened_reqs is present. If both, match_all_gened_reqs takes precedence
    part_of_term: Optional[str]  # substantive
    online: Optional[bool]  # substantive
    on_campus: Optional[bool]  # substantive
    open_sections: Optional[bool]  # NOT substantive
    # evenings: Optional[bool] # NOT substantive

    def __str__(self) -> str:
        attributes = [
            "year",
            "term",
            "keyword",
            "keyword_type",
            "instructor",
            "college",
            "subject",
            "course_id",
            "crn",
            "credit_hours",
            # "section_attributes",
            "gened_reqs",
            "match_all_gened_reqs",
            "match_any_gened_reqs",
            "part_of_term",
            "online",
            "on_campus",
            "open_sections",
            # "evenings",
        ]
        max_attr_length = max(len(attr) for attr in attributes)
        string = ""
        for attr in attributes:
            value = getattr(self, attr)
            if value is not None:
                string += "  - {:<{}}: {}\n".format(attr, max_attr_length, value)

        return string


class Query(BaseModel):
    simple_query: Optional[str]
    advanced_query: Optional[AdvancedSearchParameters]


class CourseSearchResponse(BaseModel):
    courses: List[SimpleCourse]
    query: Query
