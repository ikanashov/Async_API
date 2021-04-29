import json

from loguru import logger

import pytest

from services.film import FilmService
from models.film import SFilmGenre


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
    assert None == await film_service._get_genre_from_elastic('not_found')
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