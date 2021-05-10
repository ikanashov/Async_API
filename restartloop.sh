#!/bin/bash

# https://stackoverflow.com/questions/4060212/how-to-run-a-shell-script-when-a-file-or-directory-changes

echo "For run this tests loop you need to install entr util. apt install entr"

sudo docker-compose up --build -d

while true
do
    ls src/*.py src/models/*.py src/models/api/*.py \
       src/db/*.py src/tests/*.py src/services/*.py \
       src/api/v1/*.py src/core/*.py *.yml  |\
    entr -d -c sh -c \
    'echo Changed && 
    sudo docker-compose stop clientapicinema && 
    sudo docker-compose up --build -d clientapicinema &&
    echo "press q to exit from test loop"'\
    || break
done

sudo docker-compose down