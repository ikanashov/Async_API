#!/bin/bash

cd tests

if [ -d venv ]; then
    echo "Starting test venv"
    source ./venv/bin/activate
else
    echo "Create test venv"
    python -m venv venv
    echo "Starting test venv"
    source ./venv/bin/activate
fi

cd functional

echo "Install requirements"
pip install -r requirements.txt

./docker-entrypoint.sh
