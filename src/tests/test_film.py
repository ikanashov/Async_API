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
async def test_service_is_up(redis, elastic):
    logger.info('start test services')
    es = await elastic.cluster.health()
    assert es['status'] == 'green'
    assert await redis.ping() == b'PONG'
    logger.info('end test services')


@pytest.mark.asyncio
async def test_film_service(film_service: FilmService, read_json_data):
    logger.info('test cache film service')
    data = await read_json_data('cache_test.json')
    assert film_service.cachekey(data['testkey']['input']) == data['testkey']['output']
    await film_service._put_data_to_cache(data['testputgetdata']['key'], data['testputgetdata']['text'])
    # get data return byte, maybe must return str
    assert await film_service._get_data_from_cache(data['testputgetdata']['key']) == bytes(data['testputgetdata']['text'], 'utf-8')
    logger.info('end test cache film service')


@pytest.mark.asyncio
async def test_genre_elastic(film_service: FilmService, read_json_data):
    logger.info('test get data from genres index elastic')
    datas = await read_json_data('es_genres_data.json')
    for data in datas:
        doc = await film_service._get_genre_from_elastic(data['id'])
        logger.info(doc.dict())
        logger.info(data)
        assert doc.dict() == data
        assert doc == SFilmGenre(**data)
    assert None == await film_service._get_genre_from_elastic('not_found')
    logger.info('end test genres index')