from abc import ABC, abstractmethod
from typing import Any, List, Optional

from models.film import SFilm, SFilmGenre, SFilmPersonDetail


# done
class AbstractMovie(ABC):
    @abstractmethod
    def set_movie_index(self, movieindex: str) -> None:
        pass

    @abstractmethod
    def get_film_by_id(self, film_id: str) -> Optional[SFilm]:
        pass

    @abstractmethod
    def get_all_film(
        self,
        sort: str,
        page_size: int, page_number: int, genre_filter: str
    ) -> Optional[List[SFilm]]:
        pass

    @abstractmethod
    def search_film(
        self,
        query: str, page_size: int, page_number: int
    ) -> Optional[List[SFilm]]:
        pass


# done
class AbstractGenre(ABC):
    @abstractmethod
    def set_genre_index(self, genreindex: str) -> None:
        pass

    @abstractmethod
    def get_genre_by_id(self, genre_id: str) -> Optional[SFilmGenre]:
        pass

    @abstractmethod
    def get_all_genre(
        self,
        sort: str,
        page_size: int, page_number: int
    ) -> Optional[List[SFilmGenre]]:
        pass


# done
class AbstractPerson(ABC):
    @abstractmethod
    def set_person_index(self, personindex: str) -> None:
        pass

    @abstractmethod
    def get_person_by_id(self, person_id: str) -> Optional[SFilmPersonDetail]:
        pass

    @abstractmethod
    def get_all_person(
        self,
        sort: str,
        page_size: int, page_number: int
    ) -> Optional[List[SFilmPersonDetail]]:
        pass

    @abstractmethod
    def search_person(
        self,
        query: str, page_size: int, page_number: int
    ) -> Optional[List[SFilmPersonDetail]]:
        pass


# done
class AbstractStorage(ABC):
    @abstractmethod
    def get_data_by_id(self, index: str, id: str) -> Optional[Any]:
        pass

    def get_data(
        self,
        index: str,
        page_size: int, page_number: int,
        sort: str = None, body: str = None
    ):
        pass


# done
class AbstractCache(ABC):
    @staticmethod
    @abstractmethod
    def genkey(*args, **kwargs) -> str:
        pass

    @abstractmethod
    def get_data(self, *args, **kwargs) -> Optional[str]:
        pass

    @abstractmethod
    def put_data(self, data: str, expire: int, *args, **kwargs):
        pass


# done
class AbstractCacheStorage(ABC):
    @abstractmethod
    def get_data(self, key: str) -> Optional[str]:
        pass

    @abstractmethod
    def put_data(self, key: str, data: str, expire: int):
        pass


# done
class AbstractDataStore(ABC):
    @abstractmethod
    def get_by_id(self, index: str, id: str) -> Optional[dict]:
        pass

    @abstractmethod
    def search(
        self,
        index: str,
        page_size: int, page_number: int,
        sort: str = None, body: str = None
    ):
        pass
