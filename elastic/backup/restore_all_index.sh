#!/bin/bash
# Backup all used index in elastic for next task

ELASTIC_INDEX='movies,genres,persons'
BACKUP_LOCATION='alldata'
SNAPSHOT_NAME='snapshot_2021-04-19-17-24-16'

echo 'Restore backup for' ${ELASTIC_INDEX} 'index'

if [ -z $ELASTIC_USER ]; then ELASTIC_USER='elastic'; fi
AUTH="--user ${ELASTIC_USER}:${ELASTIC_PASSWORD}"

PORT=$(env | grep -oP "^http\.port=\K.*")
if [ -z $PORT ]; then	PORT=9200; fi

curl $AUTH -X PUT "localhost:${PORT}/_snapshot/${BACKUP_LOCATION}?pretty" -H 'Content-Type: application/json' -d'
{
  "type": "fs",
  "settings": {
    "location": "'${BACKUP_LOCATION}'",
    "compress": true
  }
}
'

echo "Restore current snapshot"
curl $AUTH -X POST \
"localhost:${PORT}/_snapshot/${BACKUP_LOCATION}/${SNAPSHOT_NAME}/_restore?pretty" \
-H 'Content-Type: application/json' -d'
{
  "indices": "'${ELASTIC_INDEX}'",
  "ignore_unavailable": true,
  "include_global_state": true
}
'