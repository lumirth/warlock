FROM python:3.9.9-slim
WORKDIR /app
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN apt-get update && \
    apt-get install -y git

RUN git clone https://github.com/lumirth/rmpy.git && \
    cd rmpy && \
    python setup.py sdist && \
    pip install .

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


