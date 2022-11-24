# pull official base image
FROM python:3.9.10-slim-bullseye
# set working directory
WORKDIR /src/webscraper
# install system dependencies
RUN apt-get update \
  && apt-get -y install libpq-dev \
  && apt-get -y install build-essential \
  && apt-get -y install firefox-esr \
  && apt-get -y install locales locales-all \
  && apt-get -y install nano
# install geckodriver
RUN  apt-get update \
  && apt-get install -y wget \
  && wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz \
  && tar -xvzf geckodriver* \
  && mv geckodriver /usr/local/bin \
  && cd /usr/local/bin \
  && chmod +x geckodriver
# Set up virtual display
RUN apt-get -qy --no-install-recommends install xvfb
RUN set -e
RUN echo "Starting X virtual framebuffer (Xvfb) in background..."
RUN Xvfb -ac :99 -screen 0 1280x1024x16 > /dev/null 2>&1 &
RUN export DISPLAY=:99
RUN exec "$@"
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install python dependencies
RUN python3 -m pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# add app
COPY . .
# Run program
CMD [ "python", "-u", "main.py"]
