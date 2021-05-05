from typing import Any, Optional

from elasticsearch import AsyncElasticsearch, NotFoundError

from core.config import config

from models.interface import AbstractStorage


es: AsyncElasticsearch = None


# Функция понадобится при внедрении зависимостей
async def get_elastic() -> AsyncElasticsearch:
    return es


async def start_elastic():
    global es
    es = AsyncElasticsearch(
        hosts=[f'{config.ELASTIC_HOST}:{config.ELASTIC_PORT}'],
        scheme=config.ELASTIC_SCHEME,
        http_auth=(config.ELASTIC_USER, config.ELASTIC_PASSWORD)
    )


async def stop_elastic():
    await es.close()


class ElasticStorage(AbstractStorage):
    def __init__(self) -> None:
        self.es: AsyncElasticsearch = es

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
        sort: str = None, body: str = None
    ):

        from_ = page_size * (page_number - 1)
        docs = await self.es.search(
            index=index,
            sort=sort,
            size=page_size,
            from_=from_,
            body=body
        )
        return docs['hits']['hits']
