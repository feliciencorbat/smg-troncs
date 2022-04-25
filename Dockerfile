# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /apps/troncs
COPY requirements.in /apps/troncs/
RUN pip-compile --upgrade
RUN pip install -r requirements.txt
COPY . /apps/troncs/