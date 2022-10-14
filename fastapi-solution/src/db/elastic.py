from abc import ABC, abstractmethod
from typing import Callable, Optional

from elasticsearch import AsyncElasticsearch, NotFoundError

es: Optional[AsyncElasticsearch] = None


async def get_elastic() -> AsyncElasticsearch:
    return es


class AsyncSearchStorage(ABC):
    @abstractmethod
    async def search(
        self, body=None, index=None, doc_type=None, params=None, headers=None
    ):
        pass

    @abstractmethod
    async def get(self, index, id, doc_type=None, params=None, headers=None):
        pass


class ElasticDB:
    def __init__(self, model: Callable, service: AsyncElasticsearch, index: str):
        self.model = model
        self.service = service
        self.index = index

    async def get_by_id(self, _id: str):
        """Запрос elasticsearch для получения информации по id"""

        try:
            raw_genre = await self.service.get(self.index, _id)
        except NotFoundError:
            return None
        return self.model(**raw_genre["_source"])
