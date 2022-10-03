from functools import lru_cache
from typing import Optional

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError, helpers
from fastapi import Depends
from models.filmwork import FilmWorkOut
from models.person import PersonOut
from services.service_base import Service


class PersonService(Service):
    index_person = "persons"
    index_films = "movies"

    async def get_person_detail(self, person_id: str, role: str) -> Optional[PersonOut]:
        film_list = []
        async for doc in helpers.async_scan(
            client=self.elastic,
            query={"_source": {"includes": ["title", role]}},
            index=self.index_films,
        ):
            film_list.append(doc["_source"])
        try:
            person = await self.elastic.get(
                self.index_person,
                person_id,
            )
        except NotFoundError:
            return
        person = PersonOut(
            id=person["_source"]["id"],
            full_name=person["_source"]["full_name"],
            role=role,
            film_ids=[],
        )
        for film in film_list:
            for actor in film["actors"]:
                if actor["id"] == person.id:
                    person.film_ids.append(film["title"])
                    break
        return person

    async def search_person(self, query: str, page_size: int, page_number: int) -> list:
        film_list = []
        persons_list = []
        async for doc in helpers.async_scan(
            client=self.elastic,
            index=self.index_person,
            query={"query": {"match": {"full_name": query}}},
        ):
            persons_list.append(
                PersonOut(
                    id=doc["_source"]["id"],
                    full_name=doc["_source"]["full_name"],
                    role=None,
                    film_ids=[],
                )
            )

        for person in persons_list:
            list_role = ["actors", "writers"]
            actors_films = []
            writers_films = []
            director_films = []
            for role in list_role:
                body = {
                    "_source": {"includes": ["id"]},
                    "query": {
                        "nested": {
                            "path": role,
                            "query": {
                                "bool": {
                                    "must": [
                                        {"match": {f"{role}.id": person.id}},
                                    ]
                                }
                            },
                        }
                    },
                }
                async for doc in helpers.async_scan(
                    client=self.elastic, index=self.index_films, query=body
                ):
                    if role == "actors":
                        actors_films.append(doc["_source"]["id"])
                    else:
                        writers_films.append(doc["_source"]["id"])
            body = {
                "_source": {"includes": ["id", "title", "imdb_rating"]},
                "query": {
                    "match": {"directors": person.full_name},
                },
            }
            async for doc in helpers.async_scan(
                client=self.elastic,
                query=body,
                index=self.index_films,
            ):
                director_films.append(doc["_source"]["id"])
                print(director_films, person.full_name)

            total_films = set()
            total_films.update(actors_films)
            total_films.update(writers_films)
            total_films.update(director_films)

            if len(actors_films) == max(
                len(actors_films), len(writers_films), len(director_films)
            ):
                person.role = "actor"
                person.film_ids = list(total_films)
                film_list.append(person)
            elif len(writers_films) == max(
                len(actors_films), len(writers_films), len(director_films)
            ):
                person.role = "writer"
                person.film_ids = list(total_films)
                film_list.append(person)
            else:
                person.role = "director"
                person.film_ids = list(total_films)
                film_list.append(person)

        persons = await self.pagination(film_list, page_size, page_number)

        return persons

    async def person_films(self, person_id: str):
        person = await self.elastic.get(self.index_person, person_id)
        person_films = []
        films_ids = []
        list_role = ["actors", "writers"]
        for role in list_role:
            body = {
                "_source": {"includes": ["id", "title", "imdb_rating"]},
                "query": {
                    "nested": {
                        "path": role,
                        "query": {
                            "bool": {
                                "must": [
                                    {"match": {f"{role}.id": person["_source"]["id"]}},
                                ]
                            }
                        },
                    }
                },
            }
            async for doc in helpers.async_scan(
                client=self.elastic, index=self.index_films, query=body
            ):
                if doc["_source"]["id"] not in films_ids:
                    films_ids.append(doc["_source"]["id"])
                    person_films.append(FilmWorkOut(**doc["_source"]))

        body = {
            "_source": {"includes": ["id", "title", "imdb_rating"]},
            "query": {
                "match": {"directors": person["_source"]["full_name"]},
            },
        }

        async for doc in helpers.async_scan(
            client=self.elastic,
            query=body,
            index=self.index_films,
        ):
            if doc["_source"]["id"] not in films_ids:
                films_ids.append(doc["_source"]["id"])
                person_films.append(FilmWorkOut(**doc["_source"]))

        return person_films


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
