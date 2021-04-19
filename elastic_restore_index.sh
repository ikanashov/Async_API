#!/bin/bash

#Восстанавливаем индексы elastic
sudo docker-compose exec -T elasticcinema01 backup/restore_all_index.sh
