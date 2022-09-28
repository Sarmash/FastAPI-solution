from functools import lru_cache

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, helpers
from fastapi import Depends
from models.genre import Genre
from services.service_base import Service


class GenreService(Service):
    """Сервис обработки запросов связанных с жанрами"""

    INDEX = 'genres'

    async def get_genres(self, page_size: int, page_query: int) -> list[Genre]:
        """Запрос к elasticsearch на получение списка жанров по заданной странице"""

        if page_query <= 0:
            page_query = 1

        page = []
        item_counter = 0

        async for doc in helpers.async_scan(
                client=self.elastic,
                index=self.INDEX,
        ):
            item_counter += 1
            if item_counter >= page_query * page_size - page_size:
                page.append(Genre(id=doc['_source']['id'], genre_name=doc['_source']['genre']))
                if len(page) == page_size:
                    return page

        if len(page) > 0:
            return page

        return page


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
