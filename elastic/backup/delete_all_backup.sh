#!/bin/bash
echo 'Command for delete all backup for ' ${ELASTIC_INDEX} 'index'

if [ -z $ELASTIC_USER ]; then ELASTIC_USER='elastic'; fi
AUTH="--user ${ELASTIC_USER}:${ELASTIC_PASSWORD}"

PORT=$(env | grep -oP "^http\.port=\K.*")
if [ -z $PORT ]; then	PORT=9200; fi

echo curl $AUTH -X DELETE "localhost:${PORT}/_snapshot/${ELASTIC_INDEX}/snap*?pretty"
