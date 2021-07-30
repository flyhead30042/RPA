# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
WORKDIR /usr/local/RPA
COPY Dockerfile  ./
COPY docker-compose.yml  ./
COPY requirements.txt  ./
COPY wtms  ./

RUN pip install -r requirements.txt