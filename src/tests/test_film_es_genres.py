import json

from elasticsearch import AsyncElasticsearch

from loguru import logger

import pytest

from core.config import config as coreconf

from db import elastic as es_db
from db import redis as redis_db

from models.film import SFilmGenre

from services.cache import Cache
from services.datastore import DataStore
from services.film import FilmService


@pytest.fixture(autouse=True)
async def setup_genres(conf, elastic, read_json_data):
    logger.info('setup genres')
    datas = await read_json_data('es_genres_data.json')
    body = ''
    for data in datas:
        index = {'index': {'_index': conf.ELASTIC_GENRE_INDEX, '_id': data['id']}}
        body += json.dumps(index) + '\n' + json.dumps(data) + '\n'
    results = await elastic.bulk(body)
    logger.info(results)
    yield datas
    logger.info('genres after loop')
    for data in datas:
        await elastic.delete(index=conf.ELASTIC_GENRE_INDEX, id=data['id'])
    logger.info('index cleared')


@pytest.mark.asyncio
async def test_genre_elastic(film_service: FilmService, read_json_data):
    logger.info('test get single data from genres index elastic')
    datas = await read_json_data('es_genres_data.json')
    for data in datas:
        doc = await film_service._get_genre_from_elastic(data['id'])
        logger.info(doc.dict())
        logger.info(data)
        assert doc.dict() == data
        assert doc == SFilmGenre(**data)
    assert await film_service._get_genre_from_elastic('not_found') is None
    logger.info('end test genres index')


@pytest.mark.asyncio
async def test_genres_elastic(film_service: FilmService, read_json_data):
    logger.info('test get many genres from elastic')
    try:
        await film_service._get_genres_from_elastic()
    except Exception as err:
        assert err.__class__ == TypeError, err

    testsconfig = await read_json_data('config_es_genres.json')
    for test in testsconfig:
        datas = await film_service._get_genres_from_elastic(
            page_size=test['page_size'], page_number=test['page_number'])
        assert len(datas) == test['page_size'], datas
        if test['body'] != '':
            assert datas == await read_json_data(test['body']), test
    logger.info('end test genres index')


@pytest.mark.asyncio
async def test_genre_elastic_storage(conf, elastic: AsyncElasticsearch, read_json_data):
    logger.info('test genre elastic storage')
    datas = await read_json_data('es_genres_data.json')
    es_db.es = elastic
    es_storage = es_db.ElasticStorage()
    for data in datas:
        doc = await es_storage.get_data_by_id(conf.ELASTIC_GENRE_INDEX, data['id'])
        assert doc == data
    assert await es_storage.get_data_by_id(conf.ELASTIC_GENRE_INDEX, 'not_found') is None
    logger.info('end test genre elastic storage')


@pytest.mark.asyncio
async def test_genres_elastic_storage(conf, elastic: AsyncElasticsearch, read_json_data):
    logger.info('test get many genres from elastic storage')
    es_db.es = elastic
    es_storage = es_db.ElasticStorage()
    try:
        await es_storage.get_data()
    except Exception as err:
        assert err.__class__ == TypeError, err

    testsconfig = await read_json_data('config_es_genres.json')
    for test in testsconfig:
        datas = await es_storage.get_data(
            index=conf.ELASTIC_GENRE_INDEX,
            page_size=test['page_size'], page_number=test['page_number'])
        assert len(datas) == test['page_size'], datas
        if test['body'] != '':
            assert datas == await read_json_data(test['body']), test
    logger.info('end test genres elastic storage')


@pytest.mark.asyncio
async def test_genre_data_store(conf, elastic, redis, read_json_data):
    logger.info('test genre data store')
    datas = await read_json_data('es_genres_data.json')
    es_db.es = elastic
    storage = es_db.ElasticStorage()
    redis_db.redis = redis
    redis_storage = redis_db.RedisStorage()
    cache = Cache(redis_storage)
    store = DataStore(storage, cache, coreconf.CLIENTAPI_CACHE_EXPIRE)
    for data in datas:
        await redis.delete(cache.genkey(index=conf.ELASTIC_GENRE_INDEX, id=data['id']))
        doc = await store.get_by_id(conf.ELASTIC_GENRE_INDEX, data['id'])
        cache_doc = await cache.get_data(index=conf.ELASTIC_GENRE_INDEX, id=data['id'])
        assert doc == data
        assert cache_doc == data
    assert await store.get_by_id(conf.ELASTIC_GENRE_INDEX, 'not_found') is None
    logger.info('end test genre data store')


@pytest.mark.asyncio
async def test_genres_data_store(conf, elastic, redis, read_json_data):
    logger.info('test genres data store')
    es_db.es = elastic
    storage = es_db.ElasticStorage()
    redis_db.redis = redis
    redis_storage = redis_db.RedisStorage()
    cache = Cache(redis_storage)
    store = DataStore(storage, cache, coreconf.CLIENTAPI_CACHE_EXPIRE)

    try:
        await store.search()
    except Exception as err:
        assert err.__class__ == TypeError, err

    testsconfig = await read_json_data('config_es_genres.json')
    for test in testsconfig:
        datas = await store.search(
            index=conf.ELASTIC_GENRE_INDEX,
            page_size=test['page_size'], page_number=test['page_number'])
        assert len(datas) == test['page_size'], datas
        if test['body'] != '':
            assert datas == await read_json_data(test['body']), test
    logger.info('end test genres data store')
