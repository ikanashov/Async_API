FROM python:3.9-slim-buster as base

FROM base as builder

RUN mkdir /install
RUN apt-get update && apt-get -y install gcc
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip && pip install --prefix=/install -r /requirements.txt

FROM base

COPY --from=builder /install /usr/local
COPY docker-entrypoint.sh /
COPY . /app
WORKDIR /app