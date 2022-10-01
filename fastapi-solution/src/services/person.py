from functools import lru_cache
from typing import Optional

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError, helpers
from fastapi import Depends
from models.person import Person, PersonFilmWork, PersonOut

from services.service_base import Service


class PersonService(Service):
    index_person = 'persons'
    index_films = 'movies'

    async def get_person_film_list(self,
                                   person_id: str) -> Optional[PersonFilmWork]:
        pass

    async def get_person_detail(self, person_id: str,
                                role: str) -> Optional[Person]:
        film_list = []
        async for doc in helpers.async_scan(
                client=self.elastic,
                query={"_source": {"includes": ["title", role]}},
                index="movies",
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
            id=person['_source']['id'],
            full_name=person['_source']['full_name'],
            role=role,
            film_ids=[]
        )
        for film in film_list:
            for actor in film['actors']:
                if actor['id'] == person.id:
                    person.film_ids.append(film['title'])
                    break
        return person

    async def search_person(self, query: str, role: str, page_size: int,
                            page_query: int) -> list:
        film_list = []
        item_counter = 0
        persons_list = []
        async for doc in helpers.async_scan(
                client=self.elastic,
                query={"_source": {"includes": ["title", role]}},
                index=self.index_films,
        ):
            film_list.append(doc["_source"])
        async for doc in helpers.async_scan(
                client=self.elastic,
                index=self.index_person,
                query={"query": {"match": {"full_name": query}}}
        ):
            item_counter += 1
            if item_counter >= page_query * page_size - page_size:
                persons_list.append(PersonOut(
                    id=doc['_source']['id'],
                    full_name=doc['_source']['full_name'],
                    role=role,
                    film_ids=[])
                )
                for film in film_list:
                    for item in film[role]:
                        for person in persons_list:
                            if item['id'] == person.id:
                                person.film_ids.append(film['title'])
                                break
                if len(persons_list) == page_size:
                    return persons_list
        return persons_list


@lru_cache()
def get_person_service(
        redise: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)) -> PersonService:
    return PersonService(redise, elastic)
