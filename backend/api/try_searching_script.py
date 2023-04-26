if __name__ == "__main__":
    from courses import SimpleCourse, AdvancedSearchParameters, DetailedSection, search_courses, initialize_professor_cache, save_professor_cache
else:
    from .courses import SimpleCourse, AdvancedSearchParameters, DetailedSection, search_courses, initialize_professor_cache, save_professor_cache
import asyncio
import shutil 
import textwrap

PROFESSOR_CACHE = initialize_professor_cache()
save_professor_cache(PROFESSOR_CACHE)


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

    import textwrap
    import shutil

    def load_courses():
        simple_courses = asyncio.run(search_courses(search_params, PROFESSOR_CACHE))
        return simple_courses

    s = load_courses()
    print_courses(s)

    def update_type_codes(courses, type_codes):
        # Loop through courses and extract type codes and descriptions
        for course in courses:
            for section in course.sections:
                for meeting in section.meetings:
                    type_codes[meeting.typeCode] = meeting.typeDesc

        # Return the updated dictionary of type codes
        return type_codes

    department_codes = [
        "ACCY",
        "ASRM",
        "ADV",
        "AE",
        "AFRO",
        "AFST",
        "AGCM",
        "AGED",
        "ALEC",
        "ABE",
        "ACE",
        "ACES",
        "AFAS",
        "AIS",
        "ANSC",
        "ANTH",
        "AHS",
        "ALS",
        "ARAB",
        "ARCH",
        "ART",
        "ARTD",
        "ARTE",
        "ARTF",
        "ARTH",
        "ARTS",
        "AAS",
        "ASST",
        "ASTR",
        "ATMS",
        "AVI",
        "BMNA",
        "BASQ",
        "BIOC",
        "BIOE",
        "BIOL",
        "BSE",
        "BIOP",
        "BCS",
        "BCOG",
        "BR",
        "BULG",
        "BUS",
        "BADM",
        "BDI",
        "BTW",
        "CHP",
        "CATL",
        "CDB",
        "CSB",
        "CAS",
        "CHBE",
        "CHEM",
        "CHIN",
        "CINE",
        "CEE",
        "CLCV",
        "CLE",
        "CIC",
        "CMN",
        "CHLH",
        "CB",
        "CWL",
        "CSE",
        "CS",
        "CW",
        "CPSC",
        "CI",
        "CZCH",
        "DANC",
        "ESE",
        "EALC",
        "ECON",
        "EDUC",
        "EPOL",
        "ERAM",
        "EOL",
        "EPS",
        "EDPR",
        "EPSY",
        "ECE",
        "ENG",
        "ENGH",
        "ETMA",
        "ENGL",
        "ESL",
        "EIL",
        "ENT",
        "ENVS",
        "ENSU",
        "EURO",
        "FIN",
        "FAA",
        "FSHN",
        "FLTE",
        "FR",
        "GSD",
        "GWS",
        "GE",
        "GS",
        "GEOG",
        "GGIS",
        "GEOL",
        "GER",
        "GMC",
        "GLBL",
        "GC",
        "GCL",
        "GRK",
        "HT",
        "HEBR",
        "HNDI",
        "HIST",
        "HORT",
        "HDFS",
        "HDES",
        "HRD",
        "HRE",
        "HCD",
        "DTX",
        "HUM",
        "IE",
        "INFO",
        "IS",
        "IB",
        "IHLT",
        "ITAL",
        "ARTJ",
        "JAPN",
        "JS",
        "JOUR",
        "KIN",
        "KOR",
        "LER",
        "LIR",
        "LA",
        "LAT",
        "LAST",
        "LLS",
        "LAW",
        "LCTL",
        "LAS",
        "LIS",
        "LGLA",
        "LING",
        "SLCL",
        "MFGE",
        "MSE",
        "MATH",
        "ME",
        "MDIA",
        "MS",
        "MACS",
        "MDVL",
        "MFST",
        "MICR",
        "MILS",
        "GRKM",
        "MCB",
        "MIP",
        "MUSE",
        "MUS",
        "MUSC",
        "NRES",
        "NS",
        "NE",
        "NEUR",
        "NPRE",
        "NUTR",
        "LEAD",
        "PATH",
        "PERS",
        "PHIL",
        "PHYS",
        "PBIO",
        "PLPA",
        "POL",
        "PS",
        "PORT",
        "PSM",
        "PSYC",
        "QUEC",
        "RST",
        "MBA",
        "REHB",
        "REL",
        "RLST",
        "RHET",
        "RMLG",
        "RSOC",
        "RUSS",
        "REES",
        "SNSK",
        "SCAN",
        "SLS",
        "SCR",
        "SLAV",
        "SOCW",
        "SOC",
        "SAME",
        "SPAN",
        "SPED",
        "SPCM",
        "SHS",
        "STAT",
        "SBC",
        "SWAH",
        "SE",
        "TSM",
        "TE",
        "TMGT",
        "THEA",
        "TAM",
        "TRST",
        "TURK",
        "UKR",
        "UP",
        "VB",
        "VCM",
        "VM",
        "WLOF",
        "WGGP",
        "WRIT",
        "YDSH",
        "COMM",
        "ESES",
        "LEIS",
        "VP",
        "ZULU",
    ]

    # search_params.year="2020"
    # type_codes = dict()
    # for code in department_codes:
    #     search_params.subject = code
    #     s = load_courses()
    #     type_codes = update_type_codes(s, type_codes)
    # import pprint
    # pprint.pprint(type_codes)


if __name__ == "__main__":
    main()
