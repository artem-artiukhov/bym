FROM python:3.7-alpine as main

# Image for local development ONLY!
LABEL maintainer="bkovalenko@intellias.com"

ENV PYTHONUNBUFFERED 1
RUN apk update && apk add --no-cache postgresql-dev gcc python3-dev musl-dev git curl

# Install requirements in a separate step for caching
COPY requirements /app/requirements

WORKDIR /app

RUN echo '10.10.56.23 gitlab.lean' >> /etc/hosts;pip install -r requirements/dev.txt
