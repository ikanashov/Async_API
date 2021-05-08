from typing import List, Optional

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

    async def search_person(self, query: str, page_size: int, page_number: int) -> Optional[List[SFilmPersonDetail]]:
        return super().search_person(query, page_size, page_number)

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

    async def search_film(
        self,
        query: str, page_size: int, page_number: int
    ) -> Optional[List[SFilm]]:
        body = ESQuery(query={'multi_match': {'query': query}}).json(by_alias=True)
        movies = await datastore.search(
            self.movieindex,
            page_size=page_size, page_number=page_number,
            sort=None, body=body
        )
        movies = [SFilm(**movie) for movie in movies]
        return movies
"""