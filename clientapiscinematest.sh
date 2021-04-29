#!/bin/bash

sudo docker-compose stop clientapicinema

sudo docker-compose rm -f clientapicinema

sudo docker-compose build clientapicinema

clear

sudo docker-compose run clientapicinema ./docker-entrypoint-test.sh
