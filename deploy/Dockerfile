FROM python:3.7-alpine

MAINTAINER Pavlo Pukach "ppukach@intellias.com"

EXPOSE 5000

ARG SSH_PRIVATE_KEY

RUN apk update && apk add --no-cache postgresql-dev gcc python3-dev musl-dev && \
    apk add curl git tzdata

# Add zone info for tzdata compatibility.
RUN ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime

# We copy just the requirements.txt first to leverage Docker cache
COPY ../requirements /app/requirements

WORKDIR /app
ENV FLASK_APP autoapp.py
ENV FLASK_ENV production

RUN pip install -r requirements/production.txt

COPY ../%7B%7Bcookiecutter.app_name%7D%7D-service /app

CMD flask db upgrade && \
    gunicorn --bind 0.0.0.0:5000 --log-level=debug --timeout 30 --max-requests 1500 {{cookiecutter.app_name}}.wsgi:app
