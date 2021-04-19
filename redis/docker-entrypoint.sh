#!/bin/sh

local_ip=$(/sbin/ip route|awk '/link/ { print $7 }')

redis-server --requirepass $REDIS_PASSWORD \
    --bind $local_ip \
    --port $REDIS_PORT \
    --loglevel notice \
    --databases 10 \
    --protected-mode yes
