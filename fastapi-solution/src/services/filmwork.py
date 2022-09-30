from functools import lru_cache
from typing import Optional

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError, helpers
from fastapi import Depends
from models.filmwork import FilmWork, FilmWorkOut
from services.service_base import Service

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class FilmService(Service):
    INDEX = "movies"
    INDEX_SIMILAR = "genres"

    async def get_by_id(self, film_id: str) -> Optional[FilmWork]:
        try:
            doc = await self.elastic.get(self.INDEX, film_id)
        except NotFoundError:
            return None
        return FilmWork(**doc["_source"])

    async def get_info_films(
        self,
        sort=None,
        genre=None,
        query=None,
        page_size: int = None,
        page_number: int = None,
    ) -> list:

        films_list = []

        if query is None and genre is None:
            body = {
                "_source": {"includes": ["id", "title", "imdb_rating"]},
            }
        elif query is None and genre:
            body = {
                "_source": {"includes": ["id", "title", "imdb_rating"]},
                "query": {"bool": {"filter": {"term": {"genre": genre.genre_name}}}},
            }
        else:
            body = {
                "_source": {"includes": ["id", "title", "imdb_rating"]},
                "query": {
                    "query_string": {"query": query},
                },
            }

        async for doc in helpers.async_scan(
            client=self.elastic,
            query=body,
            index="movies",
            scroll="5m",
            size=100,
        ):
            films_list.append(FilmWorkOut(**doc["_source"]))

        if sort:
            value = sort[1:] if sort[0] == "-" else sort
            reverse = True if value == sort[1:] else False
            films_list = sorted(
                films_list,
                key=lambda x: x.__dict__[value]
                if isinstance(x.__dict__[value], float)
                else 0,
                reverse=reverse,
            )

        films = await self.pagination(films_list, page_size, page_number)

        return films


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
