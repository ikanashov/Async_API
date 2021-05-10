import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

import uvicorn as uvicorn

from api.v1 import film, genre, person

from core.config import config
from core.logger import LOGGING

from db.elastic import start_elastic, stop_elastic
from db.redis import start_redis, stop_redis


app = FastAPI(
    # Конфигурируем название проекта. Оно будет отображаться в документации
    title=config.PROJECT_NAME,
    description=config.PROJECT_DESCRIPTION,
    version=config.PROJECT_VERSION,
    # Адрес документации в красивом интерфейсе
    docs_url='/api/openapi',
    # Адрес документации в формате OpenAPI
    openapi_url='/api/openapi.json',
    # Адрес документации в формате ReDoc
    redoc_url='/api/redoc',
    # Можно сразу сделать небольшую оптимизацию сервиса
    # и заменить стандартный JSON-сереализатор на более шуструю версию, написанную на Rust
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
async def startup():
    # Подключаемся к базам при старте сервера
    # Подключиться можем при работающем event-loop
    # Поэтому логика подключения происходит в асинхронной функции
    await start_redis()
    await start_elastic()


@app.on_event('shutdown')
async def shutdown():
    # Отключаемся от баз при выключении сервера
    await stop_redis()
    await stop_elastic()


# Фильм на пробу из базы существующих 58bff82e-d892-4799-b9b3-964e9fb26398
app.include_router(genre.router, prefix='/api/v1/genre', tags=['genre'])

app.include_router(film.router, prefix='/api/v1/film', tags=['film'])

app.include_router(person.router, prefix='/api/v1/person', tags=['person'])


if __name__ == '__main__':
    # Приложение должно запускаться с помощью команды
    # `uvicorn main:app --host 0.0.0.0 --port 8000`
    # Но таким способом проблематично запускать сервис в дебагере,
    # поэтому сервер приложения для отладки запускаем здесь
    uvicorn.run(
        'main:app',
        host=config.UVICORN_HOST,
        port=config.UVICORN_PORT,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
