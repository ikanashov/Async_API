from loguru import logger

import pytest

from services.film import FilmService


@pytest.mark.asyncio
async def test_film_service(film_service: FilmService, read_json_data):
    logger.info('test cache film service')
    data = await read_json_data('cache_test.json')
    assert film_service.cachekey(data['testkey']['input']) == data['testkey']['output']
    await film_service._put_data_to_cache(data['testputgetdata']['key'], data['testputgetdata']['text'])
    getteddata = await film_service._get_data_from_cache(data['testputgetdata']['key'])
    # get data return byte, maybe must return str
    assert getteddata == bytes(data['testputgetdata']['text'], 'utf-8')
    logger.info('end test cache film service')
