# pull official base image
FROM python:3.11.2-slim-buster

RUN apt-get update && apt-get -y install curl --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# add and install requirements
COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

# add app
COPY whatsfeed.py config.py ./
# this gets synced in the docker compose but not when building the image alone
COPY app app
COPY migrations migrations

# run server
CMD ["python", "whatsfeed.py"]