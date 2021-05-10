#!/bin/bash

cd src

if [ -d venv ]; then
    echo "Starting test venv"
    source ./venv/bin/activate
else
    echo "Create test venv"
    python -m venv venv
    echo "Starting test venv"
    source ./venv/bin/activate
fi

echo "Install requirements"
pip install -q -r requirements.txt

./docker-entrypoint-test.sh
