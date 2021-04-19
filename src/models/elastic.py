from typing import List

from pydantic import Field

from core.orjson import BaseModelOrjson


class ESQuerySearchParameters(BaseModelOrjson):
    query: str = Field('')
    search_fields: List[str] = Field(['title', 'description'], alias='fields')
    type: str = 'best_fields'


class ESQuerySearchType(BaseModelOrjson):
    multi_match: ESQuerySearchParameters = Field(ESQuerySearchParameters())


class ESQuery(BaseModelOrjson):
    query: ESQuerySearchType = Field(ESQuerySearchType())


class ESFilterGenreValue(BaseModelOrjson):
    value: str = Field('')
    boost: float = 1.0


class ESFilterGenreField(BaseModelOrjson):
    genre: ESFilterGenreValue = Field(ESFilterGenreValue())


class ESFilterTermGenre(BaseModelOrjson):
    term: ESFilterGenreField = Field(ESFilterGenreField())


class ESFilterGenre(BaseModelOrjson):
    query: ESFilterTermGenre = Field(ESFilterTermGenre())
