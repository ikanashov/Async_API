#!/bin/bash

cd tests
sudo docker-compose --env-file ../.env down

cd .. 
sudo docker-compose down