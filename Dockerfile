# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

# Setting WTMS working dir
WORKDIR /usr/local/src/wtms

# Install dependt libs
COPY requirements.txt  ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the file to workdir
COPY wtms  ./
COPY wtms/templates  ./templates