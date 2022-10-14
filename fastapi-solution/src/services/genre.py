from functools import lru_cache
from http import HTTPStatus
from typing import Optional

import core.http_exceptions as ex
from db.elastic import ElasticDB, get_elastic, AsyncSearchStorage
from db.redis import get_redis, AsyncCacheStorage
from fastapi import Depends, HTTPException
from models.genre import Genre
from services.service_base import Service


class GenreService(Service):
    """Сервис обработки запросов связанных с жанрами"""

    async def get_genres(
        self, page_size: int, page_number: int, sort: str = "asc"
    ) -> Optional[list]:
        """Запрос к elasticsearch на получение списка жанров постранично"""

        if sort != "asc" and sort != "desc":
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail=ex.BAD_SORTING_FORMAT
            )

        from_ = 0 if page_number == 1 else page_number * page_size - page_size

        body = {"sort": {"genre": {"order": sort}}}

        raw_genres = await self.elastic.search(
            index=self.INDEX_GENRES, size=page_size, body=body, from_=from_
        )

        genres = [Genre(**genre["_source"]) for genre in raw_genres["hits"]["hits"]]

        return genres

    async def get_by_id(self, genre_id: str) -> Optional[Genre]:
        """Запрос elasticsearch для получения информации по id жанра"""
        return await ElasticDB(Genre, self.elastic, self.INDEX_GENRES).get_by_id(
            genre_id
        )


@lru_cache()
def get_genre_service(
    cache: AsyncCacheStorage = Depends(get_redis),
    storage: AsyncSearchStorage = Depends(get_elastic),
) -> GenreService:
    return GenreService(cache, storage)
