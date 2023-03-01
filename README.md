# Getting started

## Prerequisites

- Docker. See [Docker installation](https://docs.docker.com/install/).

Everything else should install accordingly through the docker setup.

## Installation

1. Clone the repository
2. Open in IDE
3. `docker-compose up --build`

## Usage

- Frontend is on `localhost:8080`
- Backend is on `localhost:8000`

If things get finicky and your changes aren't being reflected, you can `docker compose down` or `docker compose rm` then `docker compose up --build` again, should fix it.

## Testing

- `docker-compose exec backend python pytest`

Testing is with pytest. [FastAPI's testing documentation](https://fastapi.tiangolo.com/tutorial/testing/) gives more details.

# Structure

- `backend` - FastAPI backend
  - FastAPI: a web framework. See [documentation](https://fastapi.tiangolo.com/)
- `frontend` - Svelte/Vite frontend
  - Svelte: a UI framework. See [documentation](https://svelte.dev/docs)
  - Vite: a build tool. See [documentation](https://vitejs.dev/guide/)

The idea is simple. You have a Svelte app deployed as a static site, and a FastAPI backend REST API providing data to the frontend. The frontend is served from a CDN, and the backend is served from a web server(that is, when finally deployed).

The backend is used to grab data from the [University's Course API](https://courses.illinois.edu/cisdocs/api), [RateMyProfessor](https://www.npmjs.com/package/@mtucourses/rate-my-professors), and [Waf's GPA Datasets](https://github.com/wadefagen/datasets). 

Note:

| Component | How frequently it updates |
| --- | --- |
| Course API | Every 10 minutes |
| RateMyProfessor | as reviews come in |
| Waf's GPA Datasets | Every semester |

Thus, it may be advantageous to store Waf's GPA Datasets in a database, and update it every semester, but query the Course API and RateMyProfessor every time the frontend is loaded.

## On the course API
There's a reason the course API only shows up in, like, two places on the entirety of GitHub. It's not exactly the easiest-to-use thing. Here are some things to note:
- The documentation will tel you to use the `cisapi` URL. Ignore it. So, wherever you'd have `courses.illinois.edu/cisapi`, use `courses.illinois.edu` instead.
- You'll have to programatically find the information you need within the XML response. The documentation is not very helpful in this regard. Use a REST client like Thunder, Postman, or Insomnia to see what the response looks like, and parse it accordingly. It may be advantageous to use a library that makes parsing XML easier.

## On RateMyProfessor
The RateMyProfessor NPM module I linked is, of course, a Node module. Thus, we'll have to figure out a way to use JS in Python, because this module looks actively maintained and fulfills our use-case spectacularly. I'm not sure how to do this, but I'm sure it's possible.

## On Waf's GPA Datasets
Waf's GPA Datasets are a CSV file that contains the GPA of every course offered at the University of Illinois. It's updated every semester. We'll need some system for updating this neatly.
