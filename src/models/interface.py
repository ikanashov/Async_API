from abc import ABC, abstractmethod
from typing import Optional


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


class AbstractCache(ABC):
    @staticmethod
    @abstractmethod
    def genkey(self, params: str) -> str:
        pass

    @abstractmethod
    def get_data(self, params: str) -> Optional[str]:
        pass

    @abstractmethod
    def put_data(self, parameter: str, data: str):
        pass


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
