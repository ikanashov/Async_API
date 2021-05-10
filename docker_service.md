# Docker-compose config

## Порядок запуска сервисов для выполнения задания
Для работы системы необходимо наличие docker и docker-compose

Для запуска проекта необходимо создать в корневой папке проекта файл .env следующего содержимого:
```shell
DOCKER_PREFIX=Async2
DOCKER_NETWORK_ADDRESS=NETWORK/MASK
REDIS_PASSWORD=<>
REDIS_PORT=6379
REDIS_API_TEST_DB=5
ELASTIC_HOST=localhost
ELASTIC_PORT=9200
ELASTIC_SCHEME=http
ELASTIC_INDEX=movies
ELASTIC_USER=elastic
ELASTIC_PASSWORD=<>
UVICORN_PORT=8011
NGINX_HTTP_PORT=8088
```

### Значение не могут содержать пробелы!

DOCKER_PREFIX - Префикс для всех сервисов docker-compose (если запускается более одного экемпляра)  
DOCKER_NETWORK_ADDRESS - Подсеть для сервисов (например 192.168.10.0/24)  
REDIS_PORT - порт который слушает REDIS внутри сети docker-compose
REDIS_PASSWORD - пароль для пользователя default (AUTH) (можно сгенерировать с помощью команды ```openssl rand -hex 32```)  
REDIS_API_TEST_DB - база в которой проходят тесты классов сервиса, должна отличаться от основной, по умолчанию 5
ELASTIC_PASSWORD - пароль elasticsearch (можно сгенерировать с помощью команды ```openssl rand -hex 32```)  
ELASTIC_HOST - имя хоста Elastic  
ELASTIC_PORT - порт Elastic  
ELASTIC_SCHEME - схема Elastic (http)  
ELASTIC_INDEX - индекс Elastic  
ELASTIC_USER - пользователь elastic  
UVICORN_PORT - порт для uvicorn сервера внутри докер сети  
NGINX_HTTP_PORT - внешний порт для веб-сервера nginx  
  

## После создания конфигурационного файла:

Для запуска всех сервисов необходимо выполнить команду ```./start```

Для начальной загрузки данных в elastic необходимо выполнить следующую команду ```./elastic_restore_index.sh```

После выполения этих команд система будет доступна по протколу http и порту указанному в NGINX_HTTP_PORT  
  
Для остановки всех сервисов необходимо выполнить команду ```./stop```
