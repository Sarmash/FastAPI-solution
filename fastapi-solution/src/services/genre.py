from functools import lru_cache
from typing import Union

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError, helpers
from fastapi import Depends
from models.genre import Genre
from services.service_base import Service


class GenreService(Service):
    """Сервис обработки запросов связанных с жанрами"""

    INDEX = "genres"

    async def get_genres(self, page_size: int, page_query: int) -> list:
        """Запрос к elasticsearch на получение списка жанров по заданной странице"""

        page = []
        item_counter = 0

        async for doc in helpers.async_scan(
            client=self.elastic,
            index=self.INDEX,
        ):
            item_counter += 1
            if item_counter >= page_query * page_size - page_size:
                page.append(
                    Genre(id=doc["_source"]["id"], genre_name=doc["_source"]["genre"])
                )
                if len(page) == page_size:
                    return page
        return page

    async def get_by_id(self, genre_id: str) -> Union[Genre, None]:
        """Запро с elasticsearch для получения информации по id жанра"""

        try:
            raw_genre = await self.elastic.get(self.INDEX, genre_id)
        except NotFoundError:
            return
        return Genre(
            id=raw_genre["_source"]["id"], genre_name=raw_genre["_source"]["genre"]
        )


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
