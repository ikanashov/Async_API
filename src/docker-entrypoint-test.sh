#!/bin/bash

if [[ -z "${REDIS_HOST}" ]]; then
    echo "REDIS_HOST is unset, maybe run locally"
else
    echo "Wait for redis ping is OK"
    python utils/wait_for_redis.py
fi


if [[ -z "${ELASTIC_HOST}" ]]; then
    echo "ELASTIC_HOST is unset, maybe run locally"
else
    echo "Wait for ES green status"
    python utils/wait_for_es.py
fi

echo "Wait for client api is answer"
python utils/wait_for_nginx.py

pytest -s -q -x
