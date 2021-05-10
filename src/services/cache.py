from hashlib import sha256
from typing import Optional

import orjson

from db.redis import get_redis_storage

from models.interface import AbstractCache, AbstractCacheStorage


class Cache(AbstractCache):
    def __init__(self, storage: AbstractCacheStorage) -> None:
        self.storage = storage

    @staticmethod
    def genkey(*args, **kwargs) -> str:
        param = [str(arg) for arg in args] + [f'{key}:{value}' for key, value in kwargs.items()]
        param = ''.join(sorted(param))
        key = sha256(param.encode()).hexdigest()
        return key

    async def get_data(self, *args, **kwargs) -> Optional[str]:
        key = self.genkey(*args, **kwargs)
        data = await self.storage.get_data(key)
        if data:
            data = orjson.loads(data)
        return data

    async def put_data(self, data: str, expire: int, *args, **kwargs):
        key = self.genkey(*args, **kwargs)
        data = orjson.dumps(data)
        await self.storage.put_data(key, data, expire)


async def get_cache() -> Cache:
    cache = Cache(storage=await get_redis_storage())
    return cache
