FROM python:3

WORKDIR /apps/troncs

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.in .
RUN pip install pip-tools
RUN pip-compile --upgrade
RUN pip install -r requirements.txt

COPY . .