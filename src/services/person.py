import json

from typing import Dict, List, Optional

from loguru import logger

from models.elastic import ESFilterGenre, ESQuery
from models.film import SFilmPersonDetail
from models.interface import AbstractDataStore, AbstractPerson

# Переделать
datastore: AbstractDataStore = None


class Person(AbstractPerson):
    def __init__(self) -> None:
        self.datastore = datastore

    async def set_person_index(self, personindex: str) -> None:
        self.personindex = personindex

    async def get_person_by_id(self, person_id: str) -> Optional[SFilmPersonDetail]:
        person = await datastore.get_by_id(self.personindex, person_id)
        if person:
            return SFilmPersonDetail(**person)

    async def get_all_person(self, sort: str, page_size: int, page_number: int) -> Optional[List[SFilmPersonDetail]]:
        return super().get_all_person(sort, page_size, page_number)

    async def search_person(
        self,
        query: str, page_size: int, page_number: int
    ) -> Optional[List[SFilmPersonDetail]]:
        query_body: Dict = {'query': {'match': {'full_name': {'query': query, 'fuzziness': 'AUTO'}}}}
        body = json.dumps(query_body)        
        persons = await datastore.search(
            self.personindex,
            page_size=page_size, page_number=page_number,
            sort=None, body=body
        )
        persons = [SFilmPersonDetail(**person) for person in persons]
        return persons

"""
    async def get_all_film(
        self,
        sort: str,
        page_size: int, page_number: int, genre_filter: str
    ) -> Optional[List[SFilm]]:

        if genre_filter is not None:
            genre_filter = ESFilterGenre(query={'term': {'genre': {'value': genre_filter}}}).json()

        movies = await datastore.search(
            self.movieindex,
            page_size=page_size, page_number=page_number,
            sort=sort, body=genre_filter
        )
        movies = [SFilm(**movie) for movie in movies]
        return movies
"""
