if __name__ == "__main__":
    from courses import SimpleCourse, AdvancedSearchParameters, DetailedSection, search_courses, initialize_professor_cache, save_professor_cache, load_gpa_data
else:
    from .courses import SimpleCourse, AdvancedSearchParameters, DetailedSection, search_courses, initialize_professor_cache, save_professor_cache, load_gpa_data
import asyncio
import shutil 
import textwrap

PROFESSOR_CACHE = initialize_professor_cache()
save_professor_cache(PROFESSOR_CACHE)
GPA_DATA = load_gpa_data()


def print_with_indent(text, indent=4, width=70):
    terminal_width = shutil.get_terminal_size().columns
    width = terminal_width - indent
    # Create a TextWrapper object with the specified indentation and width
    wrapper = textwrap.TextWrapper(initial_indent=" " * indent, subsequent_indent=" " * indent, width=width)

    # remove all newlines from the text
    text = text.replace("\n", " ")
    # Use the TextWrapper object to wrap the text
    wrapped_text = wrapper.fill(text)

    # Print the wrapped text
    print(wrapped_text)

def print_courses(simple_courses):
    for i in range(len(simple_courses)):
        print(f"{simple_courses[i].id} - {simple_courses[i].label}") if simple_courses[i].label is not None else None
        print_with_indent(f"Year: {simple_courses[i].year}") if simple_courses[i].year is not None else None
        print_with_indent(f"Term: {simple_courses[i].term}") if simple_courses[i].term is not None else None
        print_with_indent(f"Subject: {simple_courses[i].subject}") if simple_courses[i].subject is not None else None
        print_with_indent(f"Description: {simple_courses[i].description}") if simple_courses[i].description is not None else None
        print_with_indent(f"Credit Hours: {simple_courses[i].creditHours}") if simple_courses[i].creditHours is not None else None
        print_with_indent(f"Attributes: {simple_courses[i].sectionDegreeAttributes}") if simple_courses[i].sectionDegreeAttributes is not None else None
        # print_with_indent(f"Section Info: {simple_courses[i].courseSectionInformation}") if simple_courses[i].courseSectionInformation is not None else None
        print_with_indent(f"GPA : {simple_courses[i].gpa_average}") if simple_courses[i].gpa_average is not None else None
        print_with_indent(f"PROF: {simple_courses[i].prof_average}") if simple_courses[i].prof_average is not None else None

        for section in simple_courses[i].sections:
            if section.enrollmentStatus != "UNKNOWN":
                print_with_indent(f"Section: {section.sectionNumber} - POT {section.partOfTerm} - {section.enrollmentStatus} - {section.startDate} - {section.endDate}", indent=8)
            else:
                print_with_indent(f"Section: {section.sectionNumber} - POT {section.partOfTerm} - {section.startDate} - {section.endDate}", indent=8)
            for meeting in section.meetings:
                days = meeting.daysOfTheWeek.strip() if meeting.daysOfTheWeek is not None else None
                print_with_indent(f"Meeting: {meeting.typeCode} - {meeting.start} - {meeting.end} - {days} - {meeting.roomNumber} - {meeting.buildingName}", indent=12)
                for instructor in meeting.instructors:
                    print_with_indent(f"Instructor: {instructor.lastName}, {instructor.firstName}", indent=16)

# TODO: add code for match_all/match_any geneds
# - this will require filtering courses by their gen ed requirements
# TODO: rework logic to visit the individual course API page and get gened reqs from there because schedule/courses API doesn't have gened reqs
def main():
    # TODO: write tests for this
    search_params = AdvancedSearchParameters(
        year="2023",
        term="spring",
        # course_id="340",
        # online=True,
        # on_campus=True,
        subject="PHIL",
        # college="KV",
        # credit_hours="3",
        # part_of_term="A",
        # gened_reqs=["HUM"],
        # course_level="2",
        keyword_type="qs",
        keyword="minds"
        # instructor="woodley"
    )

    def load_courses():
        simple_courses = asyncio.run(search_courses(search_params, PROFESSOR_CACHE, GPA_DATA))
        return simple_courses

    s = load_courses()
    print_courses(s)


if __name__ == "__main__":
    main()
