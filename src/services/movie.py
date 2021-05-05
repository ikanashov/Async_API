from typing import List, Optional

from models.elastic import ESFilterGenre, ESQuery
from models.film import SFilm
from models.interface import AbstractDataStore, AbstractMovie

# Переделать
datastore: AbstractDataStore = None


class Movie(AbstractMovie):
    def __init__(self, movieindex: str) -> None:
        self.datastore = datastore
        self.movieindex = movieindex

    async def get_film_by_id(self, film_id: str) -> Optional[SFilm]:
        movie = await datastore.get_by_id(self.movieindex, film_id)
        if movie:
            return SFilm(**movie)

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
