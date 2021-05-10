#!/bin/bash

if [ -d /tmp ]; then
    echo "client api tests stared" >/tmp/clientapistart
fi

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

pytest -vv

if [ -f /tmp/clientapistart ]; then
    echo "delete api start file"
    rm /tmp/clientapistart
fi