# Course Warlock Data Formatting Design Document

Date: 2023-04-02

I propose we use JSON as a data format, and have two similar but different JSON objects for the data. One will be for the list view, and the other will be for the individual course view. The list view will be a list of courses, and the individual course view will be a single course. The list view will be used for the search results, and the individual course view will be used for the course's own page.

The data for a course list will be truncated, and will only contain the most important information. The data for an individual course will contain all the information we can possibly give about the course.

Data for a list of courses will be formatted as follows:

```json
{
  "courses": [
    {
      "id": "CS 222",
      "href": "https://courses.illinois.edu/schedule/2023/fall/CS/222",
      "label": "Software Design Lab",
      "credit": 1, // in hours
      "sem": "SP23", // [2 letter season][2 digit year], Ex: SP23 = Spring 2023, WI22 = Winter 2022
      "avgProf": "1.2",
      "avgGPA": "3.2",
      "description": "Design and implementation of novel software solutions. Problem identification and [...]",
      "sectInfo": "Prerequisite: CS 128; credit or [...]",
      "genEds": [], // See gened codes below.
      "sections": [
        {
          "id": "74484",
          "isOpen": true,
          "typeCode": "LCD",
          "sect": "SL1",
          "time": "11:00 AM - 12:20 PM",
          "day": "F",
          "location": "0027/1025 Campus Instructional Facility", // maybe we could add some algorithmic junk to make this more readable
          "avgProf": "1.2",
          "avgGPA": "3.2",
          "instructors": ["Woodley, M"]
        }
        // ...
      ]
    }
    // ...
  ]
}
```

Data for a single course will be formatted as follows*:

*= This is not the final format, but a work in progress. Space needs to be allotted for more detailed information about GPA and professor ratings. Maybe Reddit comments and posts as well.

```json
{
  "id": "CS 222",
  "href": "https://courses.illinois.edu/schedule/2023/fall/CS/222",
  "label": "Software Design Lab",
  "credit": 1, 
  "semester": "Spring",
  "year": "2023", 
  "avgProf": "1.2",
  "avgGPA": "3.2",
  "description": "Design and implementation of novel software solutions. Problem identification and [...]",
  "sectInfo": "Prerequisite: CS 128; credit or [...]",
  "genEds": [], // This will use full names of geneds, and not gened codes.
  "sections": [
    {
      "id": "74484",
      "isOpen": true,
      "type": "Lecture-Discussion",
      "typeCode": "LCD",
      "sect": "SL1",
      "time": "11:00 AM - 12:20 PM",
      "day": "F",
      "location": "0027/1025 Campus Instructional Facility",
      "avgProf": "1.2",
      "avgGPA": "3.2",
      "instructors": [
        {
          "name": "Woodley, M",
          "rating": "1.2",
          "gpa": "3.2",
        }
      ]
    }
    // ...
  ],
  // more goes here after sections? should we send detailed GPA data over the wire? we could try it and then split detailed GPA data into another endpoint so the user can load it on demand.
}
```

## GenEd Codes

| Name                                                             | Code    |
| ---------------------------------------------------------------- | ------- |
| Composition I                                                    | `COM`   |
| Advanced Composition                                             | `ADV`   |
| Humanities and the Arts: Literature & the Arts                   | `H-LIT` |
| Humanities and the Arts: Historical & Philosophical Perspectives | `H-HIS` |
| Natural Sciences and Technology: Life Science                    | `N-LS`  |
| Natural Sciences and Technology: Physical Science                | `N-PS`  |
| Quantitative Reasoning                                           | `QR`    |
| Social and Behavioral Sciences                                   | `SOC`   |
| Cultural Studies: Western/Comparative Cultures                   | `C-WCC` |
| Cultural Studies: Non-Western Cultures                           | `C-NWC` |
| Cultural Studies: US Minority Cultures                           | `C-MIN` |
