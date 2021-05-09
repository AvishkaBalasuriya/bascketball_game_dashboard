FROM python:latest

ENV PYTHONUNBUFFERED 1

ENV APP_HOME /matific

WORKDIR $APP_HOME

COPY . ./

RUN pip install -r $APP_HOME/requirements.txt