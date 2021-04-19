import json
import logging
import logging.config
from functools import lru_cache
from hashlib import sha256
from typing import Dict, List, Optional

from aioredis import Redis

from elasticsearch import AsyncElasticsearch, NotFoundError as ESNotFoundError

from fastapi import Depends

import orjson

from core.config import config
from core.logger import LOGGING

from db.elastic import get_elastic
from db.redis import get_redis

from models.elastic import ESFilterGenre, ESQuery
from models.film import SFilm, SFilmGenre, SFilmPersonDetail


logging.config.dictConfig(LOGGING)
logger = logging.getLogger('root')
logger.debug('Start logging')


# FilmService содержит бизнес-логику по работе с фильмами.
# Никакой магии тут нет. Обычный класс с обычными методами.
# Этот класс ничего не знает про DI — максимально сильный и независимый.
class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    # Методы для кеширования в redis
    def cachekey(self, data: str) -> str:
        return sha256(data.encode()).hexdigest()

    async def _get_data_from_cache(self, key: str) -> Optional[str]:
        data = await self.redis.get(key)
        if not data:
            return None
        return data

    async def _put_data_to_cache(self, key: str, data: str):
        await self.redis.set(key, data, expire=config.CLIENTAPI_CACHE_EXPIRE)

    # !!! Здесь начинаем работать с ручкой (слово-то какое) film !!!
    async def get_film_by_id(self, film_id: str) -> Optional[SFilm]:
        data = await self._get_data_from_cache(film_id)
        if data:
            film = SFilm.parse_raw(data)
        else:
            film = await self._get_film_from_elastic(film_id)
            if film:
                await self._put_data_to_cache(film_id, film.json())
        return film

    async def get_all_film(
        self,
        sort: str,
        page_size: int, page_number: int,
        genre_filter: str
    ) -> Optional[List[SFilm]]:

        if genre_filter is not None:
            filter_ = ESFilterGenre()
            filter_.query.term.genre.value = genre_filter
            genre_filter = filter_.json()

        key = self.cachekey(str(page_size) + str(page_number) + str(genre_filter))
        data = await self._get_data_from_cache(key)
        if data:
            films = [SFilm(**row) for row in orjson.loads(data)]
        else:
            films = await self._get_films_from_elastic(page_size, page_number, sort, body=genre_filter)
            data = orjson.dumps([film.dict() for film in films])
            await self._put_data_to_cache(key, data)
        return films

    async def search_film(self, query: str, page_size: int, page_number: int) -> Optional[List[SFilm]]:
        query_body = ESQuery()
        query_body.query.multi_match.query = query
        body = query_body.json(by_alias=True)

        key = self.cachekey(str(page_size) + str(page_number) + str(body))
        data = await self._get_data_from_cache(key)
        if data:
            films = [SFilm(**row) for row in orjson.loads(data)]
        else:
            films = await self._get_films_from_elastic(page_size, page_number, body=body)
            data = orjson.dumps([film.dict() for film in films])
            await self._put_data_to_cache(key, data)
        return films

    async def _get_films_from_elastic(
        self,
        page_size: int, page_number: int,
        sort: str = None, body: str = None
    ) -> Optional[List[SFilm]]:
        from_ = page_size * (page_number - 1)

        docs = await self.elastic.search(
            index=config.ELASTIC_INDEX,
            sort=sort,
            size=page_size,
            from_=from_,
            body=body
        )
        films = [SFilm(**doc['_source']) for doc in docs['hits']['hits']]
        return films

    async def _get_film_from_elastic(self, film_id: str) -> Optional[SFilm]:
        try:
            doc = await self.elastic.get(config.ELASTIC_INDEX, film_id)
        except ESNotFoundError:
            return None
        return SFilm(**doc['_source'])
    # !!! Здесь заканчиваем работать с ручкой (слово-то какое) film !!!

    # !!! Здесь начинаем работать с ручкой (слово-то какое) genre !!!
    async def get_genre_by_id(self, genre_id: str) -> Optional[SFilmGenre]:
        data = await self._get_data_from_cache(genre_id)
        if data:
            genre = SFilmGenre.parse_raw(data)
        else:
            genre = await self._get_genre_from_elastic(genre_id)
            if genre:
                await self._put_data_to_cache(genre_id, genre.json())
        return genre

    async def get_all_genre(
        self,
        sort: str,
        page_size: int, page_number: int,
    ) -> Optional[List[SFilmGenre]]:

        key = self.cachekey(str(page_size) + str(page_number) + str(sort))
        data = await self._get_data_from_cache(key)
        if data:
            genres = [SFilmGenre(**row) for row in orjson.loads(data)]
        else:
            genres = await self._get_genres_from_elastic(page_size, page_number, sort)
            data = orjson.dumps([genre.dict() for genre in genres])
            await self._put_data_to_cache(key, data)
        return genres

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[SFilmGenre]:
        try:
            doc = await self.elastic.get(config.ELASTIC_GENRE_INDEX, genre_id)
        except ESNotFoundError:
            return None
        return SFilmGenre(**doc['_source'])

    async def _get_genres_from_elastic(
        self,
        page_size: int, page_number: int,
        sort: str = None, body: str = '{"query": {"match_all": {}}}'
    ) -> Optional[List[SFilmGenre]]:
        from_ = page_size * (page_number - 1)

        docs = await self.elastic.search(
            index=config.ELASTIC_GENRE_INDEX,
            sort=sort,
            size=page_size,
            from_=from_,
            body=body
        )
        genres = [SFilmGenre(**doc['_source']) for doc in docs['hits']['hits']]
        return genres
    # !!! Здесь заканчиваем работать с ручкой (слово-то какое) genre !!!

    # !!! Здесь начинаем работать с ручкой (слово-то какое) person !!!
    async def get_person_by_id(self, person_id: str) -> Optional[SFilmPersonDetail]:
        data = await self._get_data_from_cache(person_id)
        if data:
            person = SFilmPersonDetail.parse_raw(data)
        else:
            person = await self._get_person_from_elastic(person_id)
            if person:
                await self._put_data_to_cache(person_id, person.json())
        return person

    async def get_all_person(
        self,
        sort: str,
        page_size: int, page_number: int,
    ) -> Optional[List[SFilmPersonDetail]]:

        key = self.cachekey(str(page_size) + str(page_number) + str(sort))
        data = await self._get_data_from_cache(key)
        if data:
            persons = [SFilmPersonDetail(**row) for row in orjson.loads(data)]
        else:
            persons = await self._get_persons_from_elastic(page_size, page_number, sort)
            data = orjson.dumps([person.dict() for person in persons])
            await self._put_data_to_cache(key, data)
        return persons

    async def search_person(self, query: str, page_size: int, page_number: int) -> Optional[List[SFilmPersonDetail]]:
        query_body: Dict = {'query': {'match': {'full_name': {'query': query, 'fuzziness': 'AUTO'}}}}
        body = json.dumps(query_body)

        key = self.cachekey(str(page_size) + str(page_number) + str(body))
        data = await self._get_data_from_cache(key)
        if data:
            persons = [SFilmPersonDetail(**row) for row in orjson.loads(data)]
        else:
            persons = await self._get_persons_from_elastic(page_size, page_number, body=body)
            data = orjson.dumps([person.dict() for person in persons])
            await self._put_data_to_cache(key, data)
        return persons

    async def _get_person_from_elastic(self, person_id: str) -> Optional[SFilmPersonDetail]:
        try:
            doc = await self.elastic.get(config.ELASTIC_PERSON_INDEX, person_id)
        except ESNotFoundError:
            return None
        return SFilmPersonDetail(**doc['_source'])

    async def _get_persons_from_elastic(
        self,
        page_size: int, page_number: int,
        sort: str = None, body: str = '{"query": {"match_all": {}}}'
    ) -> Optional[List[SFilmPersonDetail]]:
        from_ = page_size * (page_number - 1)

        docs = await self.elastic.search(
            index=config.ELASTIC_PERSON_INDEX,
            sort=sort,
            size=page_size,
            from_=from_,
            body=body
        )
        persons = [SFilmPersonDetail(**doc['_source']) for doc in docs['hits']['hits']]
        return persons
    # !!! Здесь заканчиваем работать с ручкой (слово-то какое) person !!!


# get_film_service — это провайдер FilmService.
# С помощью Depends он сообщает, что ему необходимы Redis и Elasticsearch
# Для их получения вы ранее создали функции-провайдеры в модуле db
# Используем lru_cache-декоратор, чтобы создать объект сервиса в едином экземпляре (синглтона)
@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
