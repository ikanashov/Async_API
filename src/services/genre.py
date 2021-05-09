from typing import List, Optional

from models.film import SFilmGenre
from models.interface import AbstractDataStore, AbstractGenre


class Genre(AbstractGenre):
    def __init__(self, datastore: AbstractDataStore) -> None:
        self.datastore = datastore

    def set_genre_index(self, genreindex: str) -> None:
        self.genreindex = genreindex

    async def get_genre_by_id(self, genre_id: str) -> Optional[SFilmGenre]:
        genre = await self.datastore.get_by_id(self.genreindex, genre_id)
        if genre:
            return SFilmGenre(**genre)

    async def get_all_genre(
        self,
        sort: str,
        page_size: int, page_number: int
    ) -> Optional[List[SFilmGenre]]:

        genres = await self.datastore.search(
            self.genreindex,
            page_size=page_size, page_number=page_number,
            sort=sort, body='{"query": {"match_all": {}}}'
        )
        genres = [SFilmGenre(**genre) for genre in genres]
        return genres
