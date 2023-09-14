FROM --platform=linux/amd64 python:3.9 as datasynthesizer

RUN apt-get update && apt-get install -y \
  python3-pip \
  python3-dev \
  build-essential \
  libssl-dev \
  libffi-dev \
  lib32ncurses5-dev \
  libcurl4-gnutls-dev \
  curl \
  git \
  && cd /usr/local/bin \
  && pip3 install --upgrade pip

ENV APP_HOME /datasynthesizer
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY requirements.txt $APP_HOME/
RUN pip3 install -r requirements.txt --default-timeout=100

COPY . $APP_HOME

EXPOSE 8000

CMD ["python", "./app/main.py"]
