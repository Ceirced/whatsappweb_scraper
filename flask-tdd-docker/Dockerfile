# pull official base image
FROM python:3.11.2-slim-buster as builder

RUN apt-get update && apt-get -y install curl=7.64 --no-install-recommends

FROM python:3.11.2-slim-buster

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# add and install requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# add app
COPY manage.py /usr/src/app/
# this gets synced in the docker compose but not when building the image alone
COPY src /usr/src/app/src


# run server
CMD ["python", "manage.py", "run", "-h", "0.0.0.0"]