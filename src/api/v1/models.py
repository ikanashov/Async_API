from enum import Enum
from typing import List, Optional

from fastapi import Query

from pydantic.types import UUID4

from core.config import config
from core.orjson import BaseModelOrjson


class FilmGenre(BaseModelOrjson):
    uuid: UUID4
    name: str


class FilmPerson(BaseModelOrjson):
    uuid: UUID4
    full_name: str


class FilmShort(BaseModelOrjson):
    uuid: UUID4
    title: str
    imdb_rating: float


class FilmDetail(FilmShort):
    description: Optional[str]
    genre: List[str]
    actors: Optional[List[FilmPerson]]
    writers: Optional[List[FilmPerson]]
    directors: Optional[List[FilmPerson]]


class FilmGenreDetail(FilmGenre):
    description: Optional[str]


class FilmPersonDetail(FilmPerson):
    role: List[str]
    film_ids: List[UUID4]


class Page:
    def __init__(
        self,
        page_size:  int = Query(config.CLIENTAPI_DEFAULT_PAGE_SIZE, alias='page[size]', ge=1),
        page_number: int = Query(1, alias='page[number]', ge=1)
    ) -> None:
        self.page_size = page_size
        self.page_number = page_number


class FilmSortEnum(str, Enum):
    imdb_rating_asc: str = 'imdb_rating:asc'
    imdb_rating_asc_alias: str = 'imdb_rating'
    imdb_rating_desc: str = 'imdb_rating:desc'
    imdb_rating_desc_alias: str = '-imdb_rating'


class FilmSort:
    def __init__(
        self,
        sort: FilmSortEnum = Query(
            FilmSortEnum.imdb_rating_desc_alias,
            title='Sort field',
            description='Sort field (default: "-imdb_rating", sort by imdb_rating in descending order)'
        )
    ) -> None:
        if sort == FilmSortEnum.imdb_rating_asc_alias:
            sort = FilmSortEnum.imdb_rating_asc
        if sort == FilmSortEnum.imdb_rating_desc_alias:
            sort = FilmSortEnum.imdb_rating_desc
        self.sort = sort


class FilmGenreSortEnum(str, Enum):
    genre_name_asc: str = 'name:asc'
    genre_name_asc_alias: str = 'name'
    genre_name_desc: str = 'name:desc'
    genre_name_desc_alias: str = '-name'


class FilmGenreSort:
    def __init__(
        self,
        sort: FilmGenreSortEnum = Query(
            FilmGenreSortEnum.genre_name_asc,
            title='Sort field',
            description='Sort field (default: "name:asc", sort by name in ascending order)'
        )
    ) -> None:
        if sort == FilmGenreSortEnum.genre_name_asc_alias:
            sort = FilmGenreSortEnum.genre_name_asc
        if sort == FilmGenreSortEnum.genre_name_desc_alias:
            sort = FilmGenreSortEnum.genre_name_desc
        self.sort = sort


class FilmGenreFilter:
    def __init__(
        self,
        genre_filter: Optional[str] = Query(
            None,
            title='Genre filter',
            description='Filter films by genre',
            alias='filter[genre]'
        )
    ) -> None:
        self.genre_filter = genre_filter


class FilmQuery:
    def __init__(
        self,
        query: str = Query(
            ...,
            title='Query field',
            description='Query field (search by word in title and description field)'
        )
    ) -> None:
        self.query = query


class FilmPersonQuery:
    def __init__(
        self,
        query: str = Query(
            ...,
            title='Query field',
            description='Query field (search by word in full_name field)'
        )
    ) -> None:
        self.query = query


class FilmPersonSortEnum(str, Enum):
    person_name_asc: str = 'full_name:asc'
    person_name_asc_alias: str = 'full_name'
    person_name_desc: str = 'full_name:desc'
    person_name_desc_alias: str = '-full_name'


class FilmPersonSort:
    def __init__(
        self,
        sort: FilmPersonSortEnum = Query(
            FilmPersonSortEnum.person_name_asc,
            title='Sort field',
            description='Sort field (default: "full_name:asc", sort by full_name in ascending order)'
        )
    ) -> None:
        if sort == FilmPersonSortEnum.person_name_asc_alias:
            sort = FilmPersonSortEnum.person_name_asc
        if sort == FilmPersonSortEnum.person_name_desc_alias:
            sort = FilmPersonSortEnum.person_name_desc
        # full_name is text field with raw, sort on raw field
        sort = sort.replace(':', '.raw:')
        self.sort = sort
