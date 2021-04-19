#!/bin/bash
echo 'Create backup for' ${ELASTIC_INDEX} 'index'

if [ -z $ELASTIC_USER ]; then ELASTIC_USER='elastic'; fi
AUTH="--user ${ELASTIC_USER}:${ELASTIC_PASSWORD}"

PORT=$(env | grep -oP "^http\.port=\K.*")
if [ -z $PORT ]; then	PORT=9200; fi

curl $AUTH -X PUT "localhost:${PORT}/_snapshot/${ELASTIC_INDEX}?pretty" -H 'Content-Type: application/json' -d'
{
  "type": "fs",
  "settings": {
    "location": "'${ELASTIC_INDEX}'",
    "compress": true
  }
}
'

echo "Restore current snapshot"
curl $AUTH -X POST \
"localhost:${PORT}/_snapshot/${ELASTIC_INDEX}/current/_restore?pretty" \
-H 'Content-Type: application/json' -d'
{
  "indices": "'${ELASTIC_INDEX}'",
  "ignore_unavailable": true,
  "include_global_state": true
}
'