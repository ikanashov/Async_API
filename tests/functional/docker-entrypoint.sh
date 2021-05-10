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

if [[ -z "${CLIENTAPI_SERVICE_NAME}" ]]; then
    echo "CLIENTAPI_SERVICE_NAME is unset, maybe run locally"
else
    echo "Run in docker wait for client api tests"
    sleep 5
    while  [[ -f /tmp/clientapistart ]]; do
        echo "wait for client api tests done"
        sleep 1
    done
    sleep 5
    echo "Client api cinema tests done, let's go func tests"
fi

pytest -vv
