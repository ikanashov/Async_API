from abc import ABC, abstractmethod
from typing import Any, Optional


class GetData(ABC):
    @abstractmethod
    def get_by_id(self, id: str):
        pass

    @abstractmethod
    def get_all(self, **params):
        pass

    @abstractmethod
    def search(self, **params):
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


class GetDataFromStore(ABC):
    @abstractmethod
    def get_by_id(self, id: str):
        pass

    @abstractmethod
    def search(self):
        pass
