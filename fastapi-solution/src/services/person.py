from functools import lru_cache
from typing import Union

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError, helpers
from fastapi import Depends
from models.person import Person

from services.service_base import Service


class PersonService(Service):
    index = 'persons'

    async def get_person_list(self, page_size: int, page_query: int) -> list:

        person_list = []
        item_counter = 0

        async for doc in helpers.async_scan(
            client=self.elastic,
            index=self.index,
        ):
            item_counter += 1
            if item_counter >= page_query * page_size - page_size:
                person_list.append(
                    Person(id=doc['_source']['id'],
                           full_name=doc['_source']['full_name'])
                )
                if len(person_list) == page_size:
                    return person_list
        return person_list

    async def get_person_detail(self, person_id: str) -> Union[Person, None]:
        try:
            person = await self.elastic.get(
                self.index,
                person_id,
            )
        except NotFoundError:
            return
        return Person(
            id=person['_source']['id'],
            full_name=person['_source']['full_name']
        )


@lru_cache()
def get_person_service(
        redise: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic)) -> PersonService:
    return PersonService(redise, elastic)
