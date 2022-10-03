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
        body = {"query": {"match": {"full_name": query}}}

        from_ = 0 if page_number == 1 else page_number * page_size - page_size

        raw_persons = await self.elastic.search(size=page_size, from_=from_, index=self.index_person, body=body)

        person_films_out = []

        for person in raw_persons['hits']['hits']:
            films = await self.films_for_person(person['_source']['id'])
            person_films = []

            for role, value in films.items():
                person_ids = PersonOut(id=person['_source']['id'],
                                       full_name=person['_source']['full_name'],
                                       role=role,
                                       film_ids=[film['id'] for film in value])

                if len(person_ids.film_ids) != 0:
                    person_films.append(person_ids)
            person_films_out.append(person_films)

        return person_films_out

    async def films_for_person(self, id_):
        person = await self.elastic.get(self.index_person, id_)

        full_name = person['_source']['full_name']

        body = {
            "query": {
                "multi_match": {
                    "query": full_name,
                    "type": "best_fields",
                    "fields": ["actors_names", "writers_names", "director"]
                }
            }
        }

        raw_films = await self.elastic.search(size=777, index='movies', body=body)

        films = {
            "actor": [],
            "writer": [],
            "director": []
        }

        for person in raw_films['hits']['hits']:
            person = person['_source']
            if full_name in person['actors_names']:
                films['actor'].append(person)
            elif full_name in person['writers_names']:
                films['writer'].append(person)
            elif full_name == person['director']:
                films['director'].append(person)

        return films

    async def person_films(self, person_id: str):
        films = await self.films_for_person(person_id)
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
