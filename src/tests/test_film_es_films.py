from loguru import logger

import pytest


@pytest.mark.asyncio
async def test_film_elastic_storage(conf, storage, read_json_data):
    logger.info('test film elastic storage')
    datas = await read_json_data('es_films_data.json')
    for data in datas:
        doc = await storage.get_data_by_id(conf.ELASTIC_INDEX, data['id'])
        assert doc == data
    assert await storage.get_data_by_id(conf.ELASTIC_INDEX, 'not_found') is None
    logger.info('end test film elastic storage')


@pytest.mark.asyncio
async def test_films_elastic_storage(conf, storage, read_json_data):
    logger.info('test get many films from elastic storage')
    try:
        await storage.get_data()
    except Exception as err:
        assert err.__class__ == TypeError, err
    testsconfig = await read_json_data('config_es_films.json')
    for test in testsconfig:
        datas = await storage.get_data(
            index=conf.ELASTIC_INDEX,
            page_size=test['page_size'], page_number=test['page_number'])
        assert len(datas) == test['page_size'], datas
        if test['body'] != '':
            assert datas == await read_json_data(test['body']), test
    logger.info('end test films elastic storage')


@pytest.mark.asyncio
async def test_film_data_store(conf, redis, cache, datastore, read_json_data):
    logger.info('test film data store')
    datas = await read_json_data('es_films_data.json')
    for data in datas:
        await redis.delete(cache.genkey(index=conf.ELASTIC_INDEX, id=data['id']))
        doc = await datastore.get_by_id(conf.ELASTIC_INDEX, data['id'])
        cache_doc = await cache.get_data(index=conf.ELASTIC_INDEX, id=data['id'])
        assert doc == data
        assert doc == cache_doc
    assert await datastore.get_by_id(conf.ELASTIC_INDEX, 'not_found') is None
    logger.info('end test film data store')


@pytest.mark.asyncio
async def test_films_data_store(conf, datastore, read_json_data):
    logger.info('test films data store')
    try:
        await datastore.search()
    except Exception as err:
        assert err.__class__ == TypeError, err
    testsconfig = await read_json_data('config_es_films.json')
    for test in testsconfig:
        datas = await datastore.search(
            index=conf.ELASTIC_INDEX,
            page_size=test['page_size'], page_number=test['page_number'])
        assert len(datas) == test['page_size'], datas
        if test['body'] != '':
            assert datas == await read_json_data(test['body']), test
    logger.info('end test films data store')
