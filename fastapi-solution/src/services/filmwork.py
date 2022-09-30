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
    async def get_by_id(self, film_id: str) -> Optional[FilmWork]:
        film_work = await self._film_from_cache(film_id)
        if not film_work:
            film_work = await self._get_film_from_elastic(film_id)
            if not film_work:
                return None
            await self._put_film_to_cache(film_work)
        return film_work

    async def _get_film_from_elastic(self, film_id: str) -> Optional[FilmWork]:
        try:
            doc = await self.elastic.get("movies", film_id)
        except NotFoundError:
            return None
        return FilmWork(**doc["_source"])

    async def _film_from_cache(self, film_id: str) -> Optional[FilmWork]:
        data = await self.redis.get(film_id)
        if not data:
            return None

        film_work = FilmWork.parse_raw(data)
        return film_work

    async def _put_film_to_cache(self, film_work: FilmWork):
        await self.redis.set(
            film_work.id, film_work.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS
        )

    async def get_info_films(
        self, sort=None, query=None, page_size: int = None, page_number: int = None
    ) -> list:
        films_list = []
        if query is None:
            body = {
                "_source": {"includes": ["id", "title", "imdb_rating"]},
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
