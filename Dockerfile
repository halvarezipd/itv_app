# pull official base image
FROM python:3.8-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8
ENV VIRTUAL_ENV=/opt/venv



# set working directory
WORKDIR /code/app

RUN apt-get update -qq && apt-get install -y -qq \
    # std libs
    git less nano curl \
    ca-certificates \
    wget build-essential\
    # python basic libs
    # geodjango
    gdal-bin binutils libproj-dev libgdal-dev \
    # postgresql
    libpq-dev postgresql-client && \
    apt-get clean all && rm -rf /var/apt/lists/* && rm -rf /var/cache/apt/*

# install pip
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.8 get-pip.py && rm get-pip.py
RUN pip3 install --no-cache-dir setuptools wheel -U

RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .

