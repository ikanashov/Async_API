from aioredis import Redis

from loguru import logger

import pytest

from db import redis as redis_db

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


@pytest.mark.asyncio
async def test_redis_storage(redis: Redis, read_json_data):
    logger.info('test redis storage')
    redis_db.redis = redis
    redis_storage = redis_db.RedisStorage()
    data = await read_json_data('cache_test.json')
    data = data['storagetest']
    assert await redis.delete(data['key']) == 0
    await redis_storage.put_data(data['key'], data['text'], data['expire'])
    assert await redis_storage.get_data(data['key']) == data['text']
    assert await redis.ttl(data['key']) > data['expire'] - 1
    await redis.delete(data['key'])
    logger.info('end test redis storage')
