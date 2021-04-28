#!/bin/bash

sudo docker-compose stop clientapicinema

sudo docker-compose build clientapicinema

clear

sudo docker-compose run clientapicinema pytest -v -s
