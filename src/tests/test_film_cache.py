from aioredis import Redis

from loguru import logger

import pytest

from db import redis as redis_db

from services.cache import Cache


@pytest.mark.asyncio
async def test_old_film_cache(redis, cache, read_json_data):
    logger.info('test old data cache film service')
    logger.info('test cache film service')
    data = await read_json_data('cache_test.json')
    assert cache.genkey(data['testkey']['input']) == data['testkey']['output']
    await cache.put_data(data['storagetest']['text'], data['storagetest']['expire'], data['storagetest']['key'])
    getteddata = await cache.get_data(data['storagetest']['key'])
    assert getteddata == data['storagetest']['text']
    logger.info('end test old data cache film service')


@pytest.mark.asyncio
async def test_cache_genkey(read_json_data):
    logger.info('test cache class')
    tests = await read_json_data('new_cache_test.json')
    for test in tests:
        logger.info(test['name'])
        key = Cache.genkey(*test['data']['args'], **test['data']['kwargs'])
        assert key == test['data']['key']
    logger.info('end test cache class')


@pytest.mark.asyncio
async def test_storage(redis, cache, read_json_data):
    logger.info('test redis storage')
    data = await read_json_data('cache_test.json')
    data = data['storagetest']
    await redis.delete(cache.genkey(data['key']))
    await cache.put_data(data['text'], data['expire'], data['key'])
    assert await cache.get_data(data['key']) == data['text']
    assert await redis.ttl(cache.genkey(data['key'])) > data['expire'] - 1
    await redis.delete(cache.genkey(data['key']))
    logger.info('end test redis storage')
