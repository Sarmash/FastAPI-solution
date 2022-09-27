from functools import lru_cache

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.genre import Genre
from services.service_base import Service


class GenreService(Service):

    async def get_genres(self, page: int, page_size: int) -> list[Genre]:
        """Запрос к elasticsearch на получение списка жанров постранично"""

        start = 0
        async for hits in self.scroll('genres', '2m', page_size):
            genres = [Genre(id=x['_source']['id'],
                            genre_name=x['_source']['genre']) for x in hits]
            start += 1
            if start >= page:
                return genres


@lru_cache()
def get_genre_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
