#!/bin/bash

sudo docker-compose up --build -d

cd tests

sudo docker-compose down

sudo docker-compose --env-file ../.env up --build