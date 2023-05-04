# Course Warlock

<img width="1369" alt="SCR-20230503-pwex" src="https://user-images.githubusercontent.com/65358837/236069991-e7bc5749-f40b-4d4e-8846-f946a7cfe614.png">

Students have a confusing amount of options for getting information about their courses, including [Enhanced Registration](https://banner.apps.uillinois.edu/StudentRegistrationSSB/?mepCode=1UIUC), [Classic Registration](https://apps.uillinois.edu/selfservice/), the [Course Catalog](http://catalog.illinois.edu/), the [Course Explorer](https://courses.illinois.edu/), [GPA++](https://1010labs.org/gpa), Waf’s [Gen Ed by GPA visualizations](https://waf.cs.illinois.edu/discovery/every_gen_ed_at_uiuc_by_gpa/), Waf's [Grade Disparity Between Sections visualizations](https://waf.cs.illinois.edu/discovery/grade_disparity_between_sections_at_uiuc/), [RateMyProfessors](https://www.ratemyprofessors.com/), [Coursicle](https://www.coursicle.com/), and likely more. 

Course Warlock aims to solve this. When a course *explorer* won't do, look to a course *warlock*. 

Course Warlock aims to be a comprehensive tool for streamlining the process of selecting and obtaining information about courses. Data is consolidated from various sources—RateMyProfessors ratings, historic GPA data, and the University's courses API—to help students make informed decisions about whether a course is worth taking.

## Table of Contents

- [Course Warlock](#course-warlock)
  - [Table of Contents](#table-of-contents)
- [Technical Architecture](#technical-architecture)
  - [Frontend](#frontend)
  - [Backend](#backend)
    - [Endpoints](#endpoints)
  - [Architecture](#architecture)
  - [Testing](#testing)
  - [Deployment](#deployment)
- [Installation \& Usage](#installation--usage)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Testing](#testing-1)
- [Group Members](#group-members)
- [Functionality](#functionality)
  - [Models \& Parsing](#models--parsing)
  - [The CIS API](#the-cis-api)
  - [RateMyProfessors](#ratemyprofessors)
  - [Maintenance Scripts](#maintenance-scripts)


# Technical Architecture

The project is divided into two main components: the frontend and the backend.

## Frontend

The frontend is built using **SvelteKit**, a modern UI framework, and leverages **TypeScript** to improve development speed and efficiency. The application's UI is styled with **TailwindCSS**, a utility-first CSS framework, and **DaisyUI**, a collection of tailwind CSS components. 

The frontend application is deployed as a static site and communicates with the backend to retrieve course information, ratings, and GPA data.

## Backend

The backend is developed using **FastAPI**, a Python web framework known for its performance and ease of use. Primary backend responsibilities include retrieving data from the University's courses API, RateMyProfessor, and Waf's GPA data sources. 

Datasets, such as course GPA data, are stored in a **Polars** DataFrame in memory. The maintenance script updates the dataset every semester by downloading the latest data, converting it to a feather format, and moving it to the appropriate location. The script also obtains the latest years, semesters, and other relevant data from the university.

To standardize the development environment, **Docker** is used to prevent inconsistencies between operating systems and minimize "it works on my machine" errors. This ensures portability and consistency across different systems.

### Endpoints

A comprehensive detailing of the endpoints used in the backend can be found at [backend/README.md](backend/README.md)

## Architecture 

<img width="1101" alt="image" src="https://user-images.githubusercontent.com/65358837/236199248-cff90ac7-2490-4701-93b0-9d0a14cf1129.png">

## Testing

Unit tests are implemented using **pytest** to ensure the functionality and reliability of critical components. Code style adherence and code reviews are managed through appropriate style guides and GitHub features such as branches and commenting systems.

## Deployment

The frontend is deployed on [GitHub Pages](https://pages.github.com/), while the backend is hosted on [fly.io](https://fly.io/).

# Installation & Usage

## Prerequisites

- Docker. See [Docker installation](https://docs.docker.com/install/).

Everything else should install accordingly through the docker-compose setup.

However, you may want to develop the frontend outside of the container for better reload times. To do so, make sure you have node installed and use `npm i` (or `pnpm i`, if you prefer) in the `frontend` directory. 

You may also do out-of-container development for the backend by running:

- `cd backend`
- `pip install -r requirements.txt`
- `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`

**Always check if your changes survive being containerized**, as containers are used for deployment.

## Installation

1. Clone the repository
2. Open in IDE
3. `docker compose up`

## Usage

- Frontend is on `localhost:8080`
- Backend is on `localhost:8000`

If things get finicky and your changes aren't being reflected, you can `docker compose down -v`(which removes volumes) then `docker compose up --build`. This should fix it.

For example, if a new module or library has been added to `requirements.txt`, make sure to use the above technique to make sure the container is rebuilt with the new requirements.

## Testing

- In container: `docker compose exec backend pytest`
- Outside container: `pytest`

Testing is with pytest. [FastAPI's testing documentation](https://fastapi.tiangolo.com/tutorial/testing/) gives more details.

# Group Members

Every single line of both the frontend and backend, as it currently exists, was written entirely by Lukas Unguraitis. Bangyan Shi helped develop the frontend interface. Tiancheng Shi and Parth Tyagi did not contribute.

# Functionality 

The functionality of the application, as earlier detailed in the [endpoints](#endpoints) section, is split in two:

- Simple/smart/straightforward search. A single search box that takes a user's input and attempts to parse it into a department name or identifier, course ID, CRN, semester, year, or GenEd, then returns results accordingly.
- Advanced/detailed/explicit search. A form similar to [courses.illinois.edu](https://courses.illinois.edu/search/form), allows the user to specify each of the aforementioned fields explicitly, and get results accordingly.

## Models & Parsing

The (Pydantic) models of the explanation are defined in [models.py](backend/app/models/models.py), and are most easily investigated there. As for parsing, the parsing structure works as follows:

- All queries are parsed into a `Params` object. 
- If no semester or year are specified, each defaults to the most recent year and (fall/spring) semester.
- Queries are interpreted as a comma-separated list of arguments. Arguments come in a number of forms(and are checked in the following order):
  - Colon-separated key-value pairs. `is:online`, `sem:spring`, `subj:chem`, etc. These are used to explicitly specify certain parameters within a query.
  - CRN's. 5-digit numbers.
  - Years. 4-digit numbers within the valid set of years.
  - Semesters. Fall, spring, summer, or winter. Alternatively, "fa", "sp", "su", "wi".
  - Some word or words optionally followed by a number. This is the most flexible part of parsing, as it uses fuzzy matching, allowing for typos and near-matches. This argument is parsed as follows:
    - Fuzzy match against subjects and GenEds each separately. Then match against a set of the best matches from each. Use that to determine whether to use the GenEd match or subject match. In edge cases, give subjects priority.
    - If no subjects or GenEds are matched with scores meeting a certain threshold, default to the argument being a "keyword" parameter—in effect, text to be searched in the course title and description.
      - If a keyword is a single word, set the keyword type to matching exactly. If multiple words, set to matching the exact phrase. If multiple keywords are found across the whole query, set the keyword type to match all words.

As far as the actual searching is concerned, parsing is completely separate. Parsing creates the `Params` object, and the `search_courses` function utilizes it. 

## The CIS API

By far the biggest accomplisment in this project is deciphering how to fully utilize the CIS API. It is poorly documented. Functionality like being able to search for courses with open sections, for example, is completely undocumented. For that matter, the `schedule/courses` endpoint we utilize extensively for the vast majority of the search engine's functionality isn't actually documented under the CIS Data Explorer API, but rather the out-of-date and non-functional CIS REST API documentation. All the URLs in the documentation for the CIS API are broken. 

A great deal of time was spent figuring out how to use the API and throwing stuff at the wall and tinkering until things worked. An explanation of the core of what was discovered is available at [mirth.cc/blog/deciphering-uiuc](https://mirth.cc/blog/deciphering-uiuc), and the tool written to convert the broken URLs in the documentation into their functional equivalents can be found at [mirth.cc/cisurls-web](https://mirth.cc/cisurls-web).

## RateMyProfessors

Originally, we aimed to utilize an NPM module in the backend using a clever JS-Python bridge. It worked, but the overhead required made it unbearably slow. Further, it was impossible to get all the information needed efficiently without actually unpacking the code and sending specific GraphQL queries to the RateMyProfessor API. Thus, this NPM module was completely rewritten in Python to serve the purposes of the project. It is sourced separately at [lumirth/rmpy](https://github.com/lumirth/rmpy). It is cloned and `pip install`'d manually into the docker container, into the github action tests, and locally.

The rmpy module is centrally used for its ability to fetch all the professors of a university. The professors of UIUC are then placed into an in-memory cache, allowing for them to be quickly retrieved without relying on the speed of the RateMyProfessors API. As individual student's professor reviews aren't shown, and professor's ratings change rather slowly, caching all the professors was an optimal solution for optimizing the application.

## Maintenance Scripts

A core part of the application are a set of scripts that do the following:

- Combine manual GenEd codes with the standard set, creating a dictionary that can be used to lookup the correct GenEd during parsing.
  - Since JSON is used to store these, which makes it incredibly easy to add manual fixes for the edge cases of fuzzy-matching. 
    - A user might expect 'comp sci' to reliable match 'computer science'. Unfortunately, this can't work without lowering the fuzzy matching threshold severely. 
    - Thus, a set of manual associations is made to better match a user's expectations. This set can be easily updated with the maintenance scripts.
- Fetch the list of valid years, subjects, terms, parts of term, and colleges from the university. Some of these are fetched with the CIS API, others are fetched by crawling the JSON of the university search form. 
  - By fetching these instead of having a standard hand-written set, we can ensure the application is up to date, and also make it easy to make it up-to-date.
  - These are used both in the frontend and backend. In the frontend they're saved as JSON, and in the backend they're saved as pickles. 
- Check the latest commit hash of the GPA dataset. If it is different from the commit hash we have saved, download the GPA dataset and convert it to a feather file.
  - In the backend we use Polars, which is a high-speed dataframe library akin to Pandas. Feather file format makes it especially easy and efficient to load data into memory compared to CSV.
