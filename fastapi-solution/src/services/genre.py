from functools import lru_cache
from http import HTTPStatus
from typing import Optional

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends, HTTPException
from models.genre import Genre
from services.service_base import Service


class GenreService(Service):
    """Сервис обработки запросов связанных с жанрами"""

    INDEX = "genres"

    async def get_genres(self, page_size: int, page_number: int, sort: str = "asc") -> Optional[list]:
        """Запрос к elasticsearch на получение списка жанров по заданной странице"""

        if sort != "asc" and sort != "desc":
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="incorrect sorting format")

        if page_number == 1:
            from_ = 0
        else:
            from_ = page_number*page_size - page_size

        body = {"sort": {"genre": {"order": sort}}}

        raw_genres = await self.elastic.search(index=self.INDEX, size=page_size, body=body, from_=from_)

        genres = [Genre(**genre["_source"]) for genre in raw_genres["hits"]["hits"]]

        return genres

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        """Запрос elasticsearch для получения информации по id жанра"""

        try:
            raw_genre = await self.elastic.get(self.INDEX, genre_id)
        except NotFoundError:
            return
        return Genre(**raw_genre["_source"])


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
