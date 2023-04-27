```
Last updated on 2023-04-23

Changes include:
- Add #Errors subsection under #Usage
- Add text on outside-of-container development under #Prerequisites
- Update #Structure to reflect current project frameworks
- Add note on feather files in regards to databases
- Remove commit reference for RateMyProfessor and give example in README
```

# Table of Contents

- [Table of Contents](#table-of-contents)
- [Getting started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Errors](#errors)
  - [Testing](#testing)
- [Structure](#structure)
  - [On Parsing Queries](#on-parsing-queries)
  - [On Data Formatting](#on-data-formatting)
  - [On the course API](#on-the-course-api)
  - [On RateMyProfessor](#on-ratemyprofessor)
  - [On Waf's GPA Datasets](#on-wafs-gpa-datasets)

# Getting started

## Prerequisites

- Docker. See [Docker installation](https://docs.docker.com/install/).

Everything else should install accordingly through the docker-compose setup.

However, you may want to develop the frontend outside of the container for better reload times. To do so, make sure you have node installed and use `npm i` in the `frontend` directory.

## Installation

1. Clone the repository
2. Open in IDE
3. `docker-compose up`

## Usage

- Frontend is on `localhost:8080`
- Backend is on `localhost:8000`

If things get finicky and your changes aren't being reflected, you can `docker compose down` or `docker compose rm` then `docker compose up --build` again, should fix it.

### Errors

If things get finicky and your changes aren't being reflected, you can `docker compose down -v`(which removes volumes) then `docker compose up --build`(forces a rebuild). This should fix it.

For example, if a new module or library has been added to `requirements.txt`, make sure to use the above technique to make sure it works in the container.

## Testing

- `docker compose exec backend pytest`

Testing is with pytest. [FastAPI's testing documentation](https://fastapi.tiangolo.com/tutorial/testing/) gives more details.

# Structure

- `backend` - FastAPI backend
  - FastAPI: a web framework. See [documentation](https://fastapi.tiangolo.com/)
- `frontend` - SvelteKit frontend
  - SvelteKit: a UI framework. See [documentation](https://svelte.dev/docs)
  - TailwindCSS: CSS utility class framework. See [documentation](https://tailwindcss.com/docs/)
  - DaisyUI: tailwind CSS components. See [documentation](https://daisyui.com/components/)

The idea is simple. You have a Svelte app deployed as a static site, and a FastAPI backend REST API providing data to the frontend. The frontend is served from a CDN, and the backend is served from a web server(that is, when finally deployed).

The backend is used to grab data from the [University's Course API](https://courses.illinois.edu/cisdocs/api), [RateMyProfessor](https://www.npmjs.com/package/@mtucourses/rate-my-professors), and [Waf's GPA Datasets](https://github.com/wadefagen/datasets). 

Note:

| Component | How frequently it updates |
| --- | --- |
| Course API | Every 10 minutes |
| RateMyProfessor | as reviews come in |
| Waf's GPA Datasets | Every semester |

Thus, it may be advantageous to store Waf's GPA Datasets in a database(or maybe a feather file?), and update it every semester, but query the Course API and RateMyProfessor every time the frontend is loaded.

## On Parsing Queries
There's a draft of the format by which to parse queries available in [PARSE_QUERIES.md](info/PARSE_QUERIES.md)
## On Data Formatting

A basic idea of the format for the frontend to receive the data in(and for the backend to construct the data into) can be seen in the [DATA_FORMAT.md](info/DATA_FORMAT.md) file.

## On the course API

The CIS API documentation can be found [here](https://courses.illinois.edu/cisdocs/). CIS stands for Course Information Suite. 

The CIS API's documentation is out of date. To use it, you'll have to combine some stuff from the [Data Explorer page](https://courses.illinois.edu/cisdocs/explorer) and the [CIS API documentation](https://courses.illinois.edu/cisdocs/api). Below is an example of how to fix the example links in the CIS API documentation.

On the [schedule/courses endpoint page](https://courses.illinois.edu/cisdocs/api/GET/schedule/courses) there is the following example:

```
Example Raw HTTP Request

https://courses.illinois.edu/cisapi/schedule/courses?year=2012&term=spring§ionTypeCode=LEC§ionTypeCode=Q&collegeCode=KV&creditHours=3&subject=CHEM&sessionId=1&gened=NAT&qp=atomic+structure
```

This does not work. If you look at it [here](https://courses.illinois.edu/cisapi/schedule/courses?year=2012&term=spring§ionTypeCode=LEC§ionTypeCode=Q&collegeCode=KV&creditHours=3&subject=CHEM&sessionId=1&gened=NAT&qp=atomic+structure), you'll get a 404 HTML page. 

To fix it, implement the following:

- Change “/cisapi” to “/cisapp/explorer”
- Add `.xml` before the parameters. That is, change “/courses” to “/courses.xml”

There also exists an error unique to this particular example:

- Add an “&” before the first section symbol

The resulting link is as follows:

```
Example Raw HTTP Request

https://courses.illinois.edu/cisapp/explorer/schedule/courses.xml?year=2012&term=spring&§ionTypeCode=LEC§ionTypeCode=Q&collegeCode=KV&creditHours=3&subject=CHEM&sessionId=1&gened=NAT&qp=atomic+structure
```

Take a look at it [here](https://courses.illinois.edu/cisapp/explorer/schedule/courses.xml?year=2012&term=spring&§ionTypeCode=LEC§ionTypeCode=Q&collegeCode=KV&creditHours=3&subject=CHEM&sessionId=1&gened=NAT&qp=atomic+structure). If you're in your browser, you can hit `F12` to open developer tools and examine the XML.

The assumption is that these two fixes apply to all the API endpoints, meaning that using these fixes we can access the entirety of the API and utilize the examples. **I've made a tool to do this automatically**: [mirth.cc/cisurls-web/](https://mirth.cc/cisurls-web). Note that it is not outside the realm of possibility for there to be more errors.

As another note, you can add `mode=cascade` to the URL parameters to not just show the courses/terms/departments, but all the pieces that exist inside them. Meaning, instead of just getting a list of courses inside a department, you'll also get all the sections within those courses within the same XML. This means less requests are required.

As of 2023-03-22 16:00, I have not yet received the XML schema. The link to it on the Data Explorer app page is broken, and there exist no archives of it, as far as I can tell. Until we receive this schema, it's better to **work on other portions of the project**, as waiting until we have the schema will make the implementation of the project much easier.

Update: As of 2023-03-22 17:40, I have received the XML schema. Right now I've hosted it  at [mirth.cc/cisurls-web/cisapi.xsd](https://mirth.cc/cisurls-web/cisapi.xsd).

<details>

<summary> Old course API notes </summary>

There's a reason the course API only shows up in, like, two places on the entirety of GitHub. It's not exactly the easiest-to-use thing. Here are some things to note:

The documentation will tel you to use the `cisapi` URL. Ignore it. So, wherever you'd have `courses.illinois.edu/cisapi`, use `courses.illinois.edu` instead.

You'll have to programatically find the information you need within the XML response. The documentation is not very helpful in this regard. Use a REST client like Thunder, Postman, or Insomnia to see what the response looks like, and parse it accordingly. It may be advantageous to use a library that makes parsing XML easier.

</details>

## On RateMyProfessor
The RateMyProfessor NPM module I linked is, of course, a Node module. Thus, we'll have to figure out a way to use JS in Python, because this module looks actively maintained and fulfills our use-case spectacularly. I'm not sure how to do this, but I'm sure it's possible.

Update: I've figured out how to do this. Here is a working example:

```python
import javascript

rmp = javascript.require("@mtucourses/rate-my-professors")

UNIVERSITY_ID = 'U2Nob29sLTExMTI='
results = []

results.append(rmp.default.searchTeacher('wade', UNIVERSITY_ID))
results.append(rmp.default.searchTeacher('woodley', UNIVERSITY_ID))
results.append(rmp.default.searchTeacher('michael nowak', UNIVERSITY_ID))

for result in results:
    result = result[0]
    info = rmp.default.getTeacher(result.id)
    print('Professor ', info.firstName, info.lastName + ':')
    print('RATING: ', info.avgRating)
    print('DIFFICULTY: ', info.avgDifficulty)
    print('NUM RATINGS: ', info.numRatings)
    print('PERCENT WOULD TAKE AGAIN: ', info.wouldTakeAgainPercent)
    print()
```

## On Waf's GPA Datasets
[Waf's GPA Datasets](https://github.com/wadefagen/datasets/blob/master/gpa/README.md) are a CSV file that contains the GPA of every course offered at the University of Illinois. It's updated every semester. We'll need some system for updating this neatly.
