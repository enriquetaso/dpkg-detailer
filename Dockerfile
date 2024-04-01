# syntax=docker/dockerfile:1
FROM python:3.12
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && \
    apt-get install -y iputils-ping libpq-dev curl
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/