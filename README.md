# Getting started 

## Prerequisites
- Docker. See [Docker installation](https://docs.docker.com/install/).

## Installation
1. Clone the repository
2. Open in IDE
3. `docker-compose up`

## Usage
- Frontend is on `localhost:8000`
- Backend is on `localhost:8080`

## Testing
- `docker-compose exec backend python manage.py test`

# Structure
- `backend` - Django backend
  -  Django: a web framework. See [Django documentation](https://docs.djangoproject.com/en/3.1/)
  -  Django REST Framework: a REST API framework. See [DRF documentation](https://www.django-rest-framework.org/)
- `frontend` - Svelte/Vite frontend
  - Svelte: a UI framework. See [Svelte documentation](https://svelte.dev/docs)
  - Vite: a build tool. See [Vite documentation](https://vitejs.dev/guide/)

