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
#backup name
#<snapshot_{now{yyyy-MM-dd-HH-mm-ss}}>
#%3Csnapshot_%7Bnow%7Byyyy-MM-dd-HH-mm-ss%7D%7D%3E
echo "Create snapshot"
curl $AUTH -X PUT \
"localhost:${PORT}/_snapshot/${ELASTIC_INDEX}/%3Csnapshot_%7Bnow%7Byyyy-MM-dd-HH-mm-ss%7D%7D%3E?wait_for_completion=true&pretty" \
-H 'Content-Type: application/json' -d'
{
  "indices": "'${ELASTIC_INDEX}'",
  "ignore_unavailable": true,
  "include_global_state": false,
  "metadata": {
    "taken_by": "ikanashov",
    "taken_because": "backup data"
  }
}
'
