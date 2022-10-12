from functools import lru_cache
from http import HTTPStatus
from typing import List, Optional

import core.http_exceptions as ex
import elasticsearch.exceptions
from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends, HTTPException
from models.filmwork import FilmWorkOut
from models.person import PersonOut
from services.service_base import Service


class PersonService(Service):
    """Сервис для обработки запросов по роутеру persons в elasticsearch"""

    async def get_person_detail(self, person_id: str) -> Optional[List]:
        """Получение списка всех кинопроизведений по ролям
        в которых участвовал человек по id"""

        full_name, films = await self._get_all_filmworks_for_all_roles_by_id(person_id)
        person_films = []

        for role, value in films.items():
            for film in value:
                if (
                    full_name in film["actors_names"]
                    or full_name in film["writers_names"]
                    or film["director"] == full_name
                ):
                    continue
                else:
                    value.remove(film)
            if len(value) != 0:
                person_films.append(
                    PersonOut(
                        id=person_id,
                        full_name=full_name,
                        role=role,
                        film_ids=[film["id"] for film in value],
                    )
                )

        return person_films

    async def search_person(self, query: str, page_size: int, page_number: int) -> list:
        """Поиск и сортировка совпадений имен по квери с пагинацией"""

        body = {"query": {"match": {"full_name": query}}}

        from_ = 0 if page_number == 1 else page_number * page_size - page_size

        raw_persons = await self.elastic.search(
            size=page_size, from_=from_, index=self.INDEX_PERSONS, body=body
        )

        person_films_out = []

        for person in raw_persons["hits"]["hits"]:
            _, films = await self._get_all_filmworks_for_all_roles_by_id(
                person["_source"]["id"]
            )

            for role, value in films.items():
                person_ids = PersonOut(
                    id=person["_source"]["id"],
                    full_name=person["_source"]["full_name"],
                    role=role,
                    film_ids=[film["id"] for film in value],
                )

                if len(person_ids.film_ids) != 0:
                    person_films_out.append(person_ids)

        return person_films_out

    async def _get_all_filmworks_for_all_roles_by_id(self, id_: str) -> Optional[tuple]:
        """Поиск кинопроизведений по ид с сортировкой по ролям"""

        try:
            person = await self.elastic.get(self.INDEX_PERSONS, id_)
        except elasticsearch.exceptions.NotFoundError:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=ex.PERSON_NOT_FOUND
            )

        full_name = person["_source"]["full_name"]

        body = {
            "query": {
                "multi_match": {
                    "query": full_name,
                    "type": "best_fields",
                    "fields": ["actors_names", "writers_names", "director"],
                }
            }
        }

        raw_films = await self.elastic.search(
            size=969, index=self.INDEX_MOVIES, body=body
        )

        films = {"actor": [], "writer": [], "director": []}

        for person in raw_films["hits"]["hits"]:
            person = person["_source"]
            if full_name in person["actors_names"]:
                films["actor"].append(person)

            if full_name in person["writers_names"]:
                films["writer"].append(person)

            if full_name == person["director"]:
                films["director"].append(person)

        return full_name, films

    async def person_films(self, person_id: str) -> Optional[List[FilmWorkOut]]:
        """Поиск кинопроизведений по id"""

        _, films = await self._get_all_filmworks_for_all_roles_by_id(person_id)
        person_films = []
        for role, value in films.items():
            for film in value:
                person_films.append(FilmWorkOut(**film))

        return person_films


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
