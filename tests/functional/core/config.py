import os

from pydantic import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class FuncTestSettings(BaseSettings):
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
    API_URL: str = '/api/v1/'
    NGINX_HTTP_PORT: int = 8088
    NGINX_BASE_URL: str = 'http://dev.usurt.ru'
    NGINX_URL: str = NGINX_BASE_URL + ':' + str(NGINX_HTTP_PORT)
    TEST_JSON_PATH: str = 'testdata/'

    class Config:
        # Файл .env должен находится в корне проекта
        env_file = BASE_DIR + '/../../.env'


cnf = FuncTestSettings()
