from loguru import logger

import pytest

from services.film import FilmService


@pytest.mark.asyncio
async def test_service_is_up(redis, elastic):
    logger.info('start test services')
    es = await elastic.es.cluster.health()
    assert es['status'] == 'green'
    assert await redis.ping() == b'PONG'
    logger.info('end test services')


@pytest.mark.asyncio
async def test_film_service(redis, elastic, read_json_data):
    logger.info('test cache film service')
    data = await read_json_data('cache_test.json')
    film_service: FilmService = FilmService(redis, elastic)
    assert film_service.cachekey(data['testkey']['input']) == data['testkey']['output']
    await film_service._put_data_to_cache(data['testputgetdata']['key'], data['testputgetdata']['text'])
    # get data return byte, maybe must return str
    assert await film_service._get_data_from_cache(data['testputgetdata']['key']) == bytes(data['testputgetdata']['text'], 'utf-8')
    logger.info('end test cache film service')
