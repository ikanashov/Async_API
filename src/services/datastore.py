from typing import Optional

from models.interface import AbstractCache, AbstractDataStore, AbstractStorage


class DataStore(AbstractDataStore):
    def __init__(self, storage: AbstractStorage, cache: AbstractCache, expire: int) -> None:
        self.cache = cache
        self.storage = storage
        self.expire = expire

    async def get_by_id(self, index: str, id: str) -> Optional[dict]:
        data = await self.cache.get_data(index=index, id=id)
        if data:
            return data
        else:
            data = await self.storage.get_data_by_id(index=index, id=id)
            if data:
                await self.cache.put_data(data, self.expire, index=index, id=id)
            return data

    async def search(
        self, index: str,
        page_size: int, page_number: int,
        sort: str = None, body: str = None
    ):
        datas = await self.cache.get_data(
            index=index,
            page_size=page_size, page_number=page_number,
            sort=sort, body=body
        )
        if datas:
            return datas
        else:
            datas = await self.storage.get_data(
                index=index,
                page_size=page_size, page_number=page_number,
                sort=sort, body=body
            )
            if datas:
                await self.cache.put_data(
                    datas, self.expire,
                    index=index,
                    page_size=page_size, page_number=page_number,
                    sort=sort, body=body
                )
            return datas
