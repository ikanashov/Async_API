from typing import Any, Optional

import backoff

from elasticsearch import AsyncElasticsearch, ElasticsearchException, NotFoundError

from core.config import config

from models.interface import AbstractStorage


es: AsyncElasticsearch = None


# Функция понадобится при внедрении зависимостей
async def get_elastic() -> AsyncElasticsearch:
    return es


@backoff.on_exception(backoff.expo, ElasticsearchException)
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

    @backoff.on_exception(backoff.expo, ElasticsearchException)
    async def get_data_by_id(self, index: str, id: str) -> Optional[Any]:
        try:
            data = await self.es.get_source(index, id)
        except NotFoundError:
            return None
        return data

    @backoff.on_exception(backoff.expo, ElasticsearchException)
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
        return [doc['_source'] for doc in docs['hits']['hits']]


async def get_elastic_storage() -> ElasticStorage:
    elasticstorage = ElasticStorage()
    return elasticstorage
