from aioredis import Redis

from loguru import logger

import pytest

from db import redis as redis_db


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
