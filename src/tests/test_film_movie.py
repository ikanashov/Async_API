import json

from aioredis.commands import Redis

from elasticsearch import AsyncElasticsearch

from loguru import logger

import pytest

from core.config import config as coreconf

from db import elastic as es_db
from db import redis as redis_db

from models.film import SFilm

from services import movie as mov_db
from services.cache import Cache
from services.datastore import DataStore


@pytest.fixture(autouse=True)
async def setup_films(conf, elastic: AsyncElasticsearch, read_json_data):
    logger.info('setup films')
    datas = await read_json_data('es_films_data.json')
    body = ''
    for data in datas:
        index = {'index': {'_index': conf.ELASTIC_INDEX, '_id': data['id']}}
        body += json.dumps(index) + '\n' + json.dumps(data) + '\n'
    results = await elastic.bulk(body)
    logger.info(results)
    yield datas
    logger.info('films after loop')
    for data in datas:
        await elastic.delete(index=conf.ELASTIC_INDEX, id=data['id'])
    logger.info('films index cleared')


@pytest.mark.asyncio
async def test_film_Movie_Class(conf, elastic, redis: Redis, read_json_data):
    logger.info('test film movie class')
    datas = await read_json_data('es_films_data.json')
    es_db.es = elastic
    storage = es_db.ElasticStorage()
    redis_db.redis = redis
    redis_storage = redis_db.RedisStorage()
    cache = Cache(redis_storage)
    mov_db.datastore = DataStore(storage, cache, coreconf.CLIENTAPI_CACHE_EXPIRE)
    movie = mov_db.Movie(conf.ELASTIC_INDEX)
    for data in datas:
        await redis.delete(cache.genkey(index=conf.ELASTIC_INDEX, id=data['id']))
        doc = await movie.get_film_by_id(data['id'])
        cache_doc = await cache.get_data(index=conf.ELASTIC_INDEX, id=data['id'])
        assert doc == SFilm(**data)
        assert doc == SFilm(**cache_doc)
    assert await movie.get_film_by_id('not_found') is None
    logger.info('end test film movie class')


@pytest.mark.asyncio
async def test_films_search_Movie_Class(conf, elastic, redis: Redis, read_json_data):
    logger.info('test films search movie')
    es_db.es = elastic
    storage = es_db.ElasticStorage()
    redis_db.redis = redis
    redis_storage = redis_db.RedisStorage()
    cache = Cache(redis_storage)
    mov_db.datastore = DataStore(storage, cache, coreconf.CLIENTAPI_CACHE_EXPIRE)
    movie = mov_db.Movie(conf.ELASTIC_INDEX)
    try:
        await movie.search_film()
    except Exception as err:
        assert err.__class__ == TypeError, err
    testsconfig = await read_json_data('movie_search.json')
    for test in testsconfig:
        logger.info(f"start test : {test['name']} ")
        docs = await movie.search_film(**test['parameter'])
        assert len(docs) == int(test['lenght'])
        if test['body'] != '':
            assert docs == [SFilm(**doc) for doc in await read_json_data('movie/' + test['body'])]
        logger.info(f"{test['name']} passed")
    logger.info('end test films search movie')


@pytest.mark.asyncio
async def test_films_get_all_film_Movie_Class(conf, elastic, redis: Redis, read_json_data):
    logger.info('test films get_all movie')
    es_db.es = elastic
    storage = es_db.ElasticStorage()
    redis_db.redis = redis
    redis_storage = redis_db.RedisStorage()
    cache = Cache(redis_storage)
    mov_db.datastore = DataStore(storage, cache, coreconf.CLIENTAPI_CACHE_EXPIRE)
    movie = mov_db.Movie(conf.ELASTIC_INDEX)
    try:
        await movie.get_all_film()
    except Exception as err:
        assert err.__class__ == TypeError, err
    testsconfig = await read_json_data('movie_get_all_film.json')
    for test in testsconfig:
        logger.info(f"start test : {test['name']} ")
        docs = await movie.get_all_film(**test['parameter'])
        assert len(docs) == int(test['lenght'])
        if test['body'] != '':
            assert docs == [SFilm(**doc) for doc in await read_json_data('movie/' + test['body'])]
        logger.info(f"{test['name']} passed")
    logger.info('end test films get_all movie')
