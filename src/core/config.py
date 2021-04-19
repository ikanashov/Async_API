import os
from logging import config as logging_config

from core.logger import LOGGING

from pydantic import BaseSettings


# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class FastAPISettings(BaseSettings):
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ''
    ELASTIC_HOST: str = 'localhost'
    ELASTIC_PORT: int = 9200
    ELASTIC_SCHEME: str = 'http'
    ELASTIC_USER: str = 'elastic'
    ELASTIC_PASSWORD: str = ''
    ELASTIC_INDEX: str = 'movies'
    ELASTIC_GENRE_INDEX: str = 'genres'
    ELASTIC_PERSON_INDEX: str = 'persons'
    PROJECT_NAME: str = 'movies'
    UVICORN_HOST: str = '0.0.0.0'
    UVICORN_PORT: int = 8000
    CLIENTAPI_DEFAULT_PAGE_SIZE: int = 50
    CLIENTAPI_CACHE_EXPIRE: int = 60 * 5

    class Config:
        # Файл .env должен находится в корне проекта
        env_file = BASE_DIR + '/../.env'


config = FastAPISettings()
