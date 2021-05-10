from socket import gaierror
from typing import Optional

from aioredis import Redis, RedisError, create_redis_pool

import backoff

from core.config import config

from models.interface import AbstractCacheStorage


redis: Redis = None


# Функция понадобится при внедрении зависимостей
async def get_redis() -> Redis:
    return redis


@backoff.on_exception(backoff.expo, (RedisError, gaierror))
async def start_redis():
    global redis
    redis = await create_redis_pool(
        (config.REDIS_HOST, config.REDIS_PORT),
        password=config.REDIS_PASSWORD,
        minsize=10, maxsize=20
    )


async def stop_redis():
    await redis.close()


class RedisStorage(AbstractCacheStorage):
    def __init__(self) -> None:
        self.redis: Redis = redis

    @backoff.on_exception(backoff.expo, (RedisError, gaierror))
    async def get_data(self, key: str) -> Optional[str]:
        data = await self.redis.get(key)
        if not data:
            return None
        return data.decode('utf-8')

    @backoff.on_exception(backoff.expo, (RedisError, gaierror))
    async def put_data(self, key: str, data: str, expire: int):
        await self.redis.set(key, data, expire=expire)


async def get_redis_storage() -> RedisStorage:
    redis_storage = RedisStorage()
    return redis_storage
