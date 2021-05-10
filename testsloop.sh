#!/bin/bash

# https://stackoverflow.com/questions/4060212/how-to-run-a-shell-script-when-a-file-or-directory-changes

echo "For run this tests loop you need to install entr util. apt install entr"

sudo docker-compose -f docker-compose-open-ports.yml up --build -d elasticcinema01 rediscinema

cd src
source ./venv/bin/activate

echo "Wait for redis ping is OK"
python utils/wait_for_redis.py

echo "Wait for ES green status"
python utils/wait_for_es.py


while true
do
    ls models/*.py models/api/*.py db/*.py tests/*.py services/*.py api/v1/*.py core/*.py *.py  |\
    entr -d -c sh -c \
    'echo Changed && 
    pytest -vv && 
    echo "press q to exit from test loop"'\
    || break
done

cd .. 
sudo docker-compose -f docker-compose-open-ports.yml rm -f -s elasticcinema01 rediscinema