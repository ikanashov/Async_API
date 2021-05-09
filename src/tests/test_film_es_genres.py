from loguru import logger

import pytest


@pytest.mark.asyncio
async def test_genre_elastic_storage(conf, storage, read_json_data):
    logger.info('test genre elastic storage')
    datas = await read_json_data('es_genres_data.json')
    for data in datas:
        doc = await storage.get_data_by_id(conf.ELASTIC_GENRE_INDEX, data['id'])
        assert doc == data
    assert await storage.get_data_by_id(conf.ELASTIC_GENRE_INDEX, 'not_found') is None
    logger.info('end test genre elastic storage')


@pytest.mark.asyncio
async def test_genres_elastic_storage(conf, storage, read_json_data):
    logger.info('test get many genres from elastic storage')
    try:
        await storage.get_data()
    except Exception as err:
        assert err.__class__ == TypeError, err

    testsconfig = await read_json_data('config_es_genres.json')
    for test in testsconfig:
        datas = await storage.get_data(
            index=conf.ELASTIC_GENRE_INDEX,
            page_size=test['page_size'], page_number=test['page_number'])
        assert len(datas) == test['page_size'], datas
        if test['body'] != '':
            assert datas == await read_json_data(test['body']), test
    logger.info('end test genres elastic storage')


@pytest.mark.asyncio
async def test_genre_data_store(conf, redis, cache, datastore, read_json_data):
    logger.info('test genre data store')
    datas = await read_json_data('es_genres_data.json')
    for data in datas:
        await redis.delete(cache.genkey(index=conf.ELASTIC_GENRE_INDEX, id=data['id']))
        doc = await datastore.get_by_id(conf.ELASTIC_GENRE_INDEX, data['id'])
        cache_doc = await cache.get_data(index=conf.ELASTIC_GENRE_INDEX, id=data['id'])
        assert doc == data
        assert cache_doc == data
    assert await datastore.get_by_id(conf.ELASTIC_GENRE_INDEX, 'not_found') is None
    logger.info('end test genre data store')


@pytest.mark.asyncio
async def test_genres_data_store(conf, datastore, read_json_data):
    logger.info('test genres data store')
    try:
        await datastore.search()
    except Exception as err:
        assert err.__class__ == TypeError, err
    testsconfig = await read_json_data('config_es_genres.json')
    for test in testsconfig:
        datas = await datastore.search(
            index=conf.ELASTIC_GENRE_INDEX,
            page_size=test['page_size'], page_number=test['page_number'])
        assert len(datas) == test['page_size'], datas
        if test['body'] != '':
            assert datas == await read_json_data(test['body']), test
    logger.info('end test genres data store')
