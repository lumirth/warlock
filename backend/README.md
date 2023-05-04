This section documents the available endpoints for the Course Warlock backend.

#### GET /search/simple

**Description:** This endpoint searches for courses based on a simple string query.

**Request Parameters:**

- `query` (str): The query string containing the search term.

**Response Model:**

A list of `Course` objects. Notably, the `sections` field of each `Course` object will be empty unless a specific course or CRN is specified. This is because there is no clean API-efficient way to get a search of courses from the University API along with their sections—it would require loading each course individually, which causes the final application to be unusably slow.

```json
[
  {
    "year": "string",
    "term": "string",
    "subject": "string",
    "id": "string",
    "label": "string",
    "description": "string",
    "creditHours": "string",
    "gpa_average": 0.0,
    "href": "string",
    "sections": [
      {
        "id": "string",
        "sectionNumber": "string",
        "sectionText": "string",
        "sectionNotes": "string",
        "statusCode": "string",
        "restrictions": "string",
        "partOfTerm": "string",
        "enrollmentStatus": "string",
        "startDate": "string",
        "endDate": "string",
        "meetings": [
          {
            "typeCode": "string",
            "typeDesc": "string",
            "start": "string",
            "end": "string",
            "daysOfTheWeek": "string",
            "roomNumber": "string",
            "buildingName": "string",
            "instructors": [
              {
                "lastName": "string",
                "firstName": "string",
                "department": "string",
                "avg_rating": 0.0,
                "avg_difficulty": 0.0,
                "num_ratings": 0
              }
            ]
          }
        ]
      }
    ],
    "sectionRegistrationNotes": "string",
    "sectionDegreeAttributes": "string",
    "courseSectionInformation": "string",
    "genEdAttributes": [
      {
        "id": "string",
        "name": "string"
      }
    ]
  }
]
```

#### POST /search/advanced

**Description:** This endpoint searches for courses based on a set of advanced search parameters.

**Request Body:**

A `Parameters` object.

```json
{
  "year": 0,
  "term": "string",
  "keyword": "string",
  "keyword_type": "string",
  "instructor": "string",
  "subject": "string",
  "course_id": 0,
  "crn": 0,
  "credit_hours": "string",
  "course_level": "string",
  "gened_reqs": ["string"],
  "match_all_gened_reqs": true,
  "match_any_gened_reqs": true,
  "part_of_term": "string",
  "online": true,
  "open_sections": true
}
```

**Response Model:**

A list of `Course` objects (refer to the response model in the `/search/simple` endpoint documentation).
