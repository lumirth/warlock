from typing import List, Optional
from pydantic import BaseModel
from xml.etree.ElementTree import Element
import textwrap

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

class Section(BaseModel):
    id: str
    sectionNumber: Optional[str]
    statusCode: Optional[str]
    partOfTerm: Optional[str]
    sectionStatusCode: Optional[str]
    enrollmentStatus: Optional[str]
    startDate: Optional[str]
    endDate: Optional[str]
    meetings: List[Meeting]
    
class GenEd(BaseModel):
    id: Optional[str]
    name: Optional[str]    

class Course(BaseModel):
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
    sections: Optional[List[Section]]
    sectionRegistrationNotes: Optional[str]
    sectionDegreeAttributes: Optional[str]
    courseSectionInformation: Optional[str]
    genEdAttributes: Optional[List[GenEd]]
    
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
    year: Optional[int]  # required
    term: Optional[str]  # required
    keyword: Optional[str]  # substantive
    keyword_type: Optional[str]  # NOT substantive, but required if keyword is present
    instructor: Optional[str]  # substantive
    # college: Optional[str]  # substantive
    subject: Optional[str]  # substantive
    course_id: Optional[int]  # NOT substantive
    crn: Optional[int]  # substantive, but disregards other parameters
    credit_hours: Optional[str]  # substantive
    course_level: Optional[str]  # NOT substantive
    gened_reqs: Optional[List[str]]  # substantive
    match_all_gened_reqs: Optional[bool]  # NOT substantive
    # but this or match_any_gened_reqs is required if gened_reqs is present. This is the default
    match_any_gened_reqs: Optional[bool]  # NOT substantive
    # but this or match_all_gened_reqs is required if gened_reqs is present. If both, match_all_gened_reqs takes precedence
    part_of_term: Optional[str]  # substantive
    # online: Optional[bool]  # substantive
    on_campus: Optional[bool]  # substantive
    open_sections: Optional[bool]  # NOT substantive

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
            "gened_reqs",
            "match_all_gened_reqs",
            "match_any_gened_reqs",
            "part_of_term",
            "online",
            "on_campus",
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
