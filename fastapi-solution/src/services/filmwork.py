from functools import lru_cache
from typing import Optional

from aioredis import Redis
from db.elastic import ElasticDB, get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, helpers
from fastapi import Depends
from models.filmwork import FilmWork, FilmWorkOut
from models.genre import Genre
from services.service_base import Service


class FilmService(Service):
    async def get_by_id(self, film_id: str) -> Optional[FilmWork]:
        """Запрос в elasticsearch на получение данных о фильме по id"""
        return await ElasticDB(FilmWork, self.elastic, self.INDEX_MOVIES).get_by_id(
            film_id
        )

    async def get_info_films(
        self,
        sort: Optional[str] = None,
        genre: Optional[Genre] = None,
        query: Optional[str] = None,
    ) -> list:
        """Работа с elasticsearch на получение данных о фильмах постранично"""

        films_list = []

        if query is None and genre is None:
            body = {
                "_source": {"includes": ["id", "title", "imdb_rating"]},
            }
        elif query is None and genre:
            body = {
                "_source": {"includes": ["id", "title", "imdb_rating"]},
                "query": {
                    "bool": {"filter": {"term": {self.INDEX_SIMILAR: genre.genre}}}
                },
            }
        else:
            body = {
                "_source": {"includes": ["id", "title", "imdb_rating"]},
                "query": {
                    "query_string": {"query": query},
                },
            }

        async for doc in helpers.async_scan(
            client=self.elastic, query=body, index=self.INDEX_MOVIES
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

        return films_list


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
