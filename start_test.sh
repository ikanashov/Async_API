#!/bin/bash

sudo docker-compose up --build -d

cd tests

#sudo docker-compose --env-file ../.env up --build -d
sudo docker-compose --env-file ../.env up --build