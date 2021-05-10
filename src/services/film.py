import logging
import logging.config
from functools import lru_cache

from fastapi import Depends

from core.config import config
from core.logger import LOGGING

from services.datastore import DataStore, get_data_store
from services.genre import Genre
from services.movie import Movie
from services.person import Person


logging.config.dictConfig(LOGGING)
logger = logging.getLogger('root')
logger.debug('Start logging')


class FilmService(Genre, Movie, Person):
    def __init__(self, datastore) -> None:
        self.datastore = datastore

        self.set_genre_index(config.ELASTIC_GENRE_INDEX)
        self.set_movie_index(config.ELASTIC_INDEX)
        self.set_person_index(config.ELASTIC_PERSON_INDEX)


@lru_cache()
def get_film_service(
    datastore: DataStore = Depends(get_data_store),
) -> FilmService:
    return FilmService(datastore)
