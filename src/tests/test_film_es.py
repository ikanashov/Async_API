import json

from elasticsearch import AsyncElasticsearch

from loguru import logger

import pytest

from db import elastic as es_db

@pytest.fixture(autouse=True)
async def setup_films(conf, elastic, read_json_data):
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
async def test_film_elastic(conf, elastic: AsyncElasticsearch, read_json_data):
    logger.info('test film elastic storage')
    datas = await read_json_data('es_films_data.json')
    es_db.es = elastic
    logger.info(type(es_db.es))
    es_storage = es_db.ElasticStorage()
    logger.info(type(es_storage))
    for data in datas:
        doc = await es_storage.get_data_by_id(conf.ELASTIC_INDEX, data['id'])
        assert doc == data
    assert await es_storage.get_data_by_id(conf.ELASTIC_INDEX, 'not_found') is None
    logger.info('end test film elastic storage')

"""
@pytest.mark.asyncio
async def test_genres_elastic(film_service: FilmService, read_json_data):
    logger.info('test get many films from elastic')
    try:
        await film_service._get_films_from_elastic()
    except Exception as err:
        assert err.__class__ == TypeError, err

    testsconfig = await read_json_data('config_es_films.json')
    for test in testsconfig:
        datas = await film_service._get_films_from_elastic(
            page_size=test['page_size'], page_number=test['page_number'])
        assert len(datas) == test['page_size'], datas
        if test['body'] != '':
            assert datas == await read_json_data(test['body']), test
    logger.info('end test films index')
"""