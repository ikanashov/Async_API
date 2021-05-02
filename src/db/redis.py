from typing import Optional

from aioredis import Redis

from models.interface import AbstractCacheStorage

redis: Redis = None


# Функция понадобится при внедрении зависимостей
async def get_redis() -> Redis:
    return redis


class RedisStorage(AbstractCacheStorage):
    redis: Redis = None

    def __init__(self) -> None:
        self.redis = redis

    async def get_data(self, key: str) -> Optional[str]:
        data = await self.redis.get(key)
        if not data:
            return None
        return data.decode('utf-8')

    async def put_data(self, key: str, data: str, expire: int):
        await self.redis.set(key, data, expire=expire)
