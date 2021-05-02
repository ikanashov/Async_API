from typing import Any, Optional

from elasticsearch import AsyncElasticsearch, NotFoundError

from models.interface import AbstractStorage


es: AsyncElasticsearch = None


# Функция понадобится при внедрении зависимостей
async def get_elastic() -> AsyncElasticsearch:
    return es


class ElasticStorage(AbstractStorage):
    es: AsyncElasticsearch = None
    
    def __init__(self) -> None:
        self.es = es

    async def get_data_by_id(self, index: str, id: str) -> Optional[Any]:
        try:
            data = await self.es.get_source(index, id)
        except NotFoundError:
            return None
        return data

    async def get_data(
        self,
        index: str,
        page_size: int, page_number: int,
        sort: str = None, body: str = None):
        
        from_ = page_size * (page_number - 1)
        docs = await self.es.search(
            index=index,
            sort=sort,
            size=page_size,
            from_=from_,
            body=body)
        return docs['hits']['hits']
