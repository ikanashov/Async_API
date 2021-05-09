from loguru import logger

import pytest


@pytest.mark.asyncio
async def test_person_elastic_storage(conf, storage, read_json_data):
    logger.info('test person elastic storage')
    datas = await read_json_data('es_persons_data.json')
    for data in datas:
        doc = await storage.get_data_by_id(conf.ELASTIC_PERSON_INDEX, data['id'])
        assert doc == data
    assert await storage.get_data_by_id(conf.ELASTIC_PERSON_INDEX, 'not_found') is None
    logger.info('end test person elastic storage')


@pytest.mark.asyncio
async def test_persons_elastic_storage(conf, storage, read_json_data):
    logger.info('test get many persons from elastic storage')
    try:
        await storage.get_data()
    except Exception as err:
        assert err.__class__ == TypeError, err

    testsconfig = await read_json_data('config_es_persons.json')
    for test in testsconfig:
        datas = await storage.get_data(
            index=conf.ELASTIC_PERSON_INDEX,
            page_size=test['page_size'], page_number=test['page_number'])
        assert len(datas) == test['page_size'], datas
        if test['body'] != '':
            assert datas == await read_json_data(test['body']), test
    logger.info('end test persons elastic storage')


@pytest.mark.asyncio
async def test_person_data_store(conf, redis, cache, datastore, read_json_data):
    logger.info('test person data store')
    datas = await read_json_data('es_persons_data.json')
    for data in datas:
        await redis.delete(cache.genkey(index=conf.ELASTIC_PERSON_INDEX, id=data['id']))
        doc = await datastore.get_by_id(conf.ELASTIC_PERSON_INDEX, data['id'])
        cache_doc = await cache.get_data(index=conf.ELASTIC_PERSON_INDEX, id=data['id'])
        assert doc == data
        assert cache_doc == data
    assert await datastore.get_by_id(conf.ELASTIC_PERSON_INDEX, 'not_found') is None
    logger.info('end test person data store')


@pytest.mark.asyncio
async def test_persons_data_store(conf, datastore, read_json_data):
    logger.info('test persons data store')
    try:
        await datastore.search()
    except Exception as err:
        assert err.__class__ == TypeError, err

    testsconfig = await read_json_data('config_es_persons.json')
    for test in testsconfig:
        datas = await datastore.search(
            index=conf.ELASTIC_PERSON_INDEX,
            page_size=test['page_size'], page_number=test['page_number'])
        assert len(datas) == test['page_size'], datas
        if test['body'] != '':
            assert datas == await read_json_data(test['body']), test
    logger.info('end test persons data store')
