from functools import lru_cache

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from models.genre import Genre
from services.service_base import Service


class GenreService(Service):
    """Сервис обработки запросов связанных с жанрами"""

    INDEX = 'genres'

    async def get_by_id(self, genre_id: str) -> Genre:
        try:
            raw_genre = await self.elastic.get(self.INDEX, genre_id)
        except NotFoundError:
            return
        return Genre(id=raw_genre['_source']['id'],
                     genre_name=raw_genre['_source']['genre'])


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
