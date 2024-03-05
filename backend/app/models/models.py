from typing import List, Optional
from pydantic import BaseModel
from xml.etree.ElementTree import Element
import textwrap

class Instructor(BaseModel):
    lastName: str
    firstName: str
    department: Optional[str] = None
    avg_rating: Optional[float] = None
    avg_difficulty: Optional[float] = None
    num_ratings: Optional[int] = None

class Meeting(BaseModel):
    typeCode: Optional[str] = None
    typeDesc: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None
    daysOfTheWeek: Optional[str] = None
    roomNumber: Optional[str] = None
    buildingName: Optional[str] = None
    instructors: List[Instructor]

class Section(BaseModel):
    id: str
    sectionNumber: Optional[str] = None
    sectionText: Optional[str] = None
    sectionNotes: Optional[str] = None
    statusCode: Optional[str] = None
    restrictions: Optional[str] = None
    partOfTerm: Optional[str] = None
    enrollmentStatus: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    meetings: List[Meeting]
    
class GenEd(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None    

class Course(BaseModel):
    year: Optional[str] = None
    term: Optional[str] = None
    subject: Optional[str] = None
    id: Optional[str] = None
    label: Optional[str] = None
    description: Optional[str] = None
    creditHours: Optional[str] = None
    gpa_average: Optional[float] = None
    prof_average: Optional[float] = None
    href: Optional[str]  = None
    sections: Optional[List[Section]] = None
    sectionRegistrationNotes: Optional[str] = None
    sectionDegreeAttributes: Optional[str] = None
    courseSectionInformation: Optional[str] = None
    genEdAttributes: Optional[List[GenEd]] = None
    
    def __hash__(self):
        return hash(self.href)

    @classmethod
    def from_xml_element(cls, course_xml: Element) -> "Course":
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
        
    def __str__(self) -> str:
        def print_with_indent(text, indent=4, width=130):
            # Create a TextWrapper object with the specified indentation and width
            wrapper = textwrap.TextWrapper(initial_indent=" " * indent, subsequent_indent=" " * indent, width=width)
            # Remove all newlines from the text
            text = text.replace("\n", " ")
            # Use the TextWrapper object to wrap the text
            return wrapper.fill(text) + "\n"

        # Start with basic course information
        course_str = f"{self.id} - {self.label}\n" if self.label is not None else ""
        course_str += print_with_indent(f"Year: {self.year}") if self.year is not None else ""
        course_str += print_with_indent(f"Term: {self.term}") if self.term is not None else ""
        course_str += print_with_indent(f"Subject: {self.subject}") if self.subject is not None else ""
        course_str += print_with_indent(f"Description: {self.description}") if self.description is not None else ""
        course_str += print_with_indent(f"Credit Hours: {self.creditHours}") if self.creditHours is not None else ""
        course_str += print_with_indent(f"GPA : {self.gpa_average}") if self.gpa_average is not None else ""
        course_str += print_with_indent(f"PROF: {self.prof_average}") if self.prof_average is not None else ""
        if self.genEdAttributes:
            for gened in self.genEdAttributes:
                course_str += print_with_indent(f"GenEd: {gened.name} - {gened.id}", indent=4)

        # Add information about sections
        if self.sections:
            for section in self.sections:
                if section.enrollmentStatus != "UNKNOWN":
                    course_str += print_with_indent(f"Section: {section.id} - {section.sectionNumber} - POT {section.partOfTerm} - {section.enrollmentStatus} - {section.startDate} - {section.endDate}", indent=8)
                else:
                    course_str += print_with_indent(f"Section: {section.id} - {section.sectionNumber} - POT {section.partOfTerm} - {section.startDate} - {section.endDate}", indent=8)
                # Add information about meetings within each section
                if section.meetings:
                    for meeting in section.meetings:
                        days = meeting.daysOfTheWeek.strip() if meeting.daysOfTheWeek is not None else None
                        course_str += print_with_indent(f"Meeting: {meeting.typeCode} - {meeting.start} - {meeting.end} - {days} - {meeting.roomNumber} - {meeting.buildingName}", indent=12)
                        # Add information about instructors within each meeting
                        if meeting.instructors:
                            for instructor in meeting.instructors:
                                course_str += print_with_indent(f"Instructor: {instructor.lastName}, {instructor.firstName}", indent=16)
        return course_str

class Parameters(BaseModel):
    year: Optional[int] = None  # required
    term: Optional[str] = None  # required
    keyword: Optional[str] = None  # substantive
    keyword_type: Optional[str] = None  # NOT substantive, but required if keyword is present
    instructor: Optional[str] = None  # substantive
    subject: Optional[str] = None  # substantive
    course_id: Optional[int] = None  # NOT substantive
    crn: Optional[int] = None  # substantive, but disregards other parameters
    credit_hours: Optional[str] = None  # substantive
    course_level: Optional[str] = None  # NOT substantive
    gened_reqs: Optional[List[str]] = None  # substantive
    match_all_gened_reqs: Optional[bool] = None  # NOT substantive
    # but this or match_any_gened_reqs is required if gened_reqs is present. This is the default
    match_any_gened_reqs: Optional[bool] = None  # NOT substantive
    # but this or match_all_gened_reqs is required if gened_reqs is present. If both, match_all_gened_reqs takes precedence
    part_of_term: Optional[str] = None  # substantive
    online: Optional[bool] = None  # substantive
    open_sections: Optional[bool] = None  # NOT substantive

    def __str__(self) -> str:
        attributes = [
            "year",
            "term",
            "keyword",
            "keyword_type",
            "instructor",
            "subject",
            "course_id",
            "crn",
            "credit_hours",
            "gened_reqs",
            "match_all_gened_reqs",
            "match_any_gened_reqs",
            "part_of_term",
            "online",
            "open_sections",
        ]
        max_attr_length = max(len(attr) for attr in attributes)
        string = ""
        for attr in attributes:
            value = getattr(self, attr)
            if value is not None:
                string += "  - {:<{}}: {}\n".format(attr, max_attr_length, value)

        return string
    
class CourseSearchResponse(BaseModel):
    courses: List[Course]
    query: Parameters
