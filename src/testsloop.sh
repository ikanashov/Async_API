#!/bin/bash

echo "For run this loop needs entr util. apt install entr"

while true;
    do
    ls db/*.py tests/*.py | entr -d sh -c \
    'clear && echo Changed && pytest -vv';
    # 'clear && echo Changed && pytest -s tests/test_film_es.py';
    done
    
    