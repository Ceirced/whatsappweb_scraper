# define base image as python slim-buster.
FROM python:3.9-slim-buster as base

## start builder stage.

# this is the first stage of the build.
# it will install all requirements.
# FROM base as builder
# install all packages for chromedriver: https://gist.github.com/varyonic/dea40abcf3dd891d204ef235c6e8dd79
RUN apt-get update 
RUN apt-get install -y xvfb gnupg wget curl unzip --no-install-recommends
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
    apt-get update -y 
RUN apt-get install -y google-chrome-stable 

# copy any python requirements file into the install directory and install all python requirements.
COPY requirements_whatsfeed_scraper.txt requirements.txt
RUN pip install --upgrade --no-cache-dir -r requirements.txt
RUN rm requirements.txt # remove requirements file from container.

# copy the source code into /app and move into that directory.
ARG USER_ID
ARG GROUP_ID

RUN addgroup --gid $GROUP_ID user
RUN useradd --uid $USER_ID --gid $GROUP_ID -ms /bin/bash user
USER user
WORKDIR /home/user/app

COPY src /home/user/app
## end builder stage.

#####

## start base stage.

# this is the image this is run.
CMD ["python", "/home/user/app/webscraper.py"]
## end base stage.
