#!/bin/bash

# https://stackoverflow.com/questions/4060212/how-to-run-a-shell-script-when-a-file-or-directory-changes

echo "For run this loop needs entr util. apt install entr"


source ./venv/bin/activate

while true;
    do
    ls models/*.py models/api/*.py db/*.py tests/*.py services/*.py api/v1/*.py core/*.py *.py  |\
     entr -d sh -c \
    'clear && echo Changed && pytest -vv';
    # 'clear && echo Changed && pytest -s tests/test_film_es.py';
    done
