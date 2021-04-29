import json

from loguru import logger

import pytest

from services.film import FilmService
from models.film import SFilmPersonDetail


@pytest.fixture(autouse=True)
async def setup_persons(conf, elastic, read_json_data):
    logger.info('setup persons')
    datas = await read_json_data('es_persons_data.json')
    body = ''
    for data in datas:
        index = {'index': {'_index': conf.ELASTIC_PERSON_INDEX, '_id': data['id']}}
        body += json.dumps(index) + '\n' + json.dumps(data) + '\n'
    results = await elastic.bulk(body)
    logger.info(results)
    yield datas
    logger.info('persons after loop')
    for data in datas:
        await elastic.delete(index=conf.ELASTIC_PERSON_INDEX, id=data['id'])
    logger.info('person index cleared')


@pytest.mark.asyncio
async def test_genre_elastic(film_service: FilmService, read_json_data):
    logger.info('test get single data from perosns index elastic')
    datas = await read_json_data('es_persons_data.json')
    for data in datas:
        doc = await film_service._get_person_from_elastic(data['id'])
        assert doc == SFilmPersonDetail(**data)
    assert None == await film_service._get_person_from_elastic('not_found')
    logger.info('end test persons index')


@pytest.mark.asyncio
async def test_genres_elastic(film_service: FilmService, read_json_data):
    logger.info('test get many persons from elastic')
    try:
        await film_service._get_persons_from_elastic()
    except Exception as err:
        assert err.__class__ == TypeError, err

    testsconfig = await read_json_data('config_es_persons.json')
    for test in testsconfig:
        datas = await film_service._get_persons_from_elastic(
            page_size=test['page_size'], page_number=test['page_number'])
        assert len(datas) == test['page_size'], datas
        if test['body'] != '':
            assert datas == await read_json_data(test['body']), test
    logger.info('end test persons index')
