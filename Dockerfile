# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /apps/troncs

# RUN addgroup --system app_troncs && adduser --system --group app_troncs

COPY requirements.in /apps/troncs/
RUN pip install pip-tools
RUN pip-compile --upgrade
RUN pip install -r requirements.txt
COPY . /apps/troncs/

# chown all the files to the app user
# RUN chown -R app_troncs:app_troncs /apps/troncs

# change to the app user
# USER app_troncs