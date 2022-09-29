from functools import lru_cache
from typing import Optional

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from models.filmwork import FilmWork

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    # get_by_id возвращает объект фильма. Он опционален, так как фильм может отсутствовать в базе
    async def get_by_id(self, film_id: str) -> Optional[FilmWork]:
        # Пытаемся получить данные из кеша, потому что оно работает быстрее
        film_work = await self._film_from_cache(film_id)
        if not film_work:
            # Если фильма нет в кеше, то ищем его в Elasticsearch
            film_work = await self._get_film_from_elastic(film_id)
            if not film_work:
                # Если он отсутствует в Elasticsearch, значит, фильма вообще нет в базе
                return None
            # Сохраняем фильм в кеш
            await self._put_film_to_cache(film_work)
        return film_work

    async def _get_film_from_elastic(self, film_id: str) -> Optional[FilmWork]:
        try:
            doc = await self.elastic.get("movies", film_id)
        except NotFoundError:
            return None
        return FilmWork(**doc["_source"])

    async def _film_from_cache(self, film_id: str) -> Optional[FilmWork]:
        # Пытаемся получить данные о фильме из кеша, используя команду get
        # https://redis.io/commands/get
        data = await self.redis.get(film_id)
        if not data:
            return None

        # pydantic предоставляет удобное API для создания объекта моделей из json
        film_work = FilmWork.parse_raw(data)
        return film_work

    async def _put_film_to_cache(self, film_work: FilmWork):
        # Сохраняем данные о фильме, используя команду set.
        # Выставляем время жизни кеша — 5 минут.
        # https://redis.io/commands/set.
        # pydantic позволяет сериализовать модель в json.
        await self.redis.set(
            film_work.id, film_work.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS
        )

    async def get_info_films(self, sort: str) -> list:
        if sort[0] == "-":
            sort = sort[1:]
            order = "desc"
        else:
            order = "asc"
        res = await self.elastic.search(
            index="movies",
            body={
                "size": 999,
                "sort": {sort: {"order": order}},
                "_source": {"includes": ["id", "title", "imdb_rating"]},
            },
        )
        result = [i["_source"] for i in res["hits"]["hits"]]
        return result


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
