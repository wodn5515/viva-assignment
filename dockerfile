FROM python:3.11-slim-buster

RUN apt-get update
RUN apt-get install -y gcc python3-dev
RUN apt-get install -y default-libmysqlclient-dev

RUN mkdir -p /app

ENV PYTHONUNBUFFERED=1

WORKDIR /app

ADD requirements.txt requirements.txt

RUN pip --no-cache-dir install -r requirements.txt

ADD . /app
