import asyncio
import json
import os
import sys
from pathlib import Path

import aioredis

from elasticsearch import AsyncElasticsearch

from loguru import logger

import pytest

# this need to add script start dir to import path
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from core.config import config

from db import elastic as es_db
from db import redis as redis_db

from services.cache import Cache
from services.datastore import DataStore
from services.film import FilmService


TEST_JSON_PATH = 'tests/data/'


@pytest.fixture(scope='session')
async def conf():
    return config


# https://github.com/pytest-dev/pytest-asyncio/issues/68
# https://github.com/pytest-dev/pytest-asyncio/issues/171
# https://github.com/pytest-dev/pytest-asyncio
@pytest.fixture(scope='session')
def event_loop():
    """Create an instance of the default event loop for each test case."""
    logger.info('start event loop')
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def redis():
    logger.info('start redis')
    redis = await aioredis.create_redis_pool(
        (config.REDIS_HOST, config.REDIS_PORT),
        password=config.REDIS_PASSWORD,
        minsize=10, maxsize=20
    )
    yield redis
    logger.info('redis after yield')
    # aioredis must close like this
    # https://aioredis.readthedocs.io/en/v1.3.0/examples.html
    redis.close()
    await redis.wait_closed()


@pytest.fixture(scope='session')
async def elastic():
    logger.info('start elastic')
    elastic = AsyncElasticsearch(
        hosts=[f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'],
        scheme=config.ELASTIC_SCHEME,
        http_auth=(config.ELASTIC_USER, config.ELASTIC_PASSWORD)
    )
    yield elastic
    logger.info('elastic after yield')
    await elastic.close()


@pytest.fixture(scope='session')
async def storage(elastic):
    logger.info('setup storage')
    es_db.es = elastic
    storage = es_db.ElasticStorage()
    yield storage
    logger.info('end setup storage')


@pytest.fixture(scope='session')
async def cache(redis):
    logger.info('setup cache')
    redis_db.redis = redis
    redis_storage = redis_db.RedisStorage()
    cache = Cache(redis_storage)
    yield cache
    logger.info('end setup cache')


@pytest.fixture(scope='session')
async def datastore(storage, cache, conf):
    logger.info('setup datastor')
    datastore = DataStore(storage, cache, conf.CLIENTAPI_CACHE_EXPIRE)
    yield datastore
    logger.info('end setup datastore')


@pytest.fixture(scope='session', autouse=True)
async def setup_films(conf, elastic, read_json_data):
    logger.info('setup films')
    datas = await read_json_data('es_films_data.json')
    body = ''
    for data in datas:
        index = {'index': {'_index': conf.ELASTIC_INDEX, '_id': data['id']}}
        body += json.dumps(index) + '\n' + json.dumps(data) + '\n'
    results = await elastic.bulk(body, refresh='wait_for')
    logger.info(results)
    yield datas
    logger.info('films after loop')
    for data in datas:
        await elastic.delete(index=conf.ELASTIC_INDEX, id=data['id'])
    logger.info('films index cleared')


@pytest.fixture(scope='session', autouse=True)
async def setup_genres(conf, elastic, read_json_data):
    logger.info('setup genres')
    datas = await read_json_data('es_genres_data.json')
    body = ''
    for data in datas:
        index = {'index': {'_index': conf.ELASTIC_GENRE_INDEX, '_id': data['id']}}
        body += json.dumps(index) + '\n' + json.dumps(data) + '\n'
    results = await elastic.bulk(body, refresh='wait_for')
    logger.info(results)
    yield datas
    logger.info('genres after loop')
    for data in datas:
        await elastic.delete(index=conf.ELASTIC_GENRE_INDEX, id=data['id'])
    logger.info('index cleared')


@pytest.fixture(scope='session', autouse=True)
async def setup_persons(conf, elastic, read_json_data):
    logger.info('setup persons')
    datas = await read_json_data('es_persons_data.json')
    body = ''
    for data in datas:
        index = {'index': {'_index': conf.ELASTIC_PERSON_INDEX, '_id': data['id']}}
        body += json.dumps(index) + '\n' + json.dumps(data) + '\n'
    results = await elastic.bulk(body, refresh='wait_for')
    logger.info(results)
    yield datas
    logger.info('persons after loop')
    for data in datas:
        await elastic.delete(index=conf.ELASTIC_PERSON_INDEX, id=data['id'])
    logger.info('person index cleared')


# https://stackoverflow.com/questions/50329629/how-to-access-a-json-filetest-data-like-config-json-in-conftest-py
@pytest.fixture(scope='session')
async def read_json_data(request):
    async def inner(datafilename: str) -> dict:
        jsonpath = Path(Path.cwd(), TEST_JSON_PATH, datafilename)
        with jsonpath.open() as fp:
            data = json.load(fp)
        return data
    return inner


@pytest.fixture
async def film_service(redis, elastic):
    logger.info('start film_service')
    film_service: FilmService = FilmService(redis, elastic)
    return film_service
