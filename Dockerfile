# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /apps/troncs
COPY requirements.txt /apps/troncs/
RUN pip install -r requirements.txt
COPY . /apps/troncs/