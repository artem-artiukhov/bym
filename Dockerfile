FROM python:3.7-alpine as main

# Image for local development ONLY!
LABEL maintainer="artem.artiukhov@chromeriver.com"

ENV PYTHONUNBUFFERED 1
RUN apk update && apk add --no-cache postgresql-dev gcc python3-dev musl-dev git curl

# Install requirements in a separate step for caching
COPY requirements /app/requirements

WORKDIR /app

RUN pip install -r requirements/dev.txt
