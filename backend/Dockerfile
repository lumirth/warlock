FROM python:3.9
WORKDIR /app
COPY requirements.txt .
ARG PIP_CACHE
RUN --mount=type=cache,target=/root/.cache/pip,from=$PIP_CACHE pip install -r requirements.txt
COPY . .
EXPOSE 8000