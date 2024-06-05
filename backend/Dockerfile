# backend/Dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./main.py /app
COPY ./requirements.txt /app

RUN pip install -r requirements.txt
