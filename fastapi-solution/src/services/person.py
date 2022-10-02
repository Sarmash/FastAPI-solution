from functools import lru_cache
from typing import Optional

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch, NotFoundError, helpers
from fastapi import Depends
from models.person import FilmWorkOut, PersonOut

from services.service_base import Service


class PersonService(Service):
    index_person = 'persons'
    index_films = 'movies'

    async def get_person_film_list(self,
                                   person_id: str,) -> Optional[list]:
        """
        Возвращает фильмы по конкретной персоне
        """
        person = await self.elastic.get(self.index_person, person_id)
        person_films = []
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
                                    {"match": {f"{role}.id": person["_source"][
                                        "id"]}},
                                ]
                            }
                        },
                    }
                },
            }
            async for doc in helpers.async_scan(
                    client=self.elastic, index=self.index_films, query=body
            ):
                person_films.append(FilmWorkOut(**doc["_source"]))

        body = {
            "_source": {"includes": ["id", "title", "imdb_rating"]},
            "query": {
                "match": {"director": person["_source"]["full_name"]},
            },
        }

        async for doc in helpers.async_scan(
                client=self.elastic,
                query=body,
                index=self.index_films,
        ):
            for film in person_films:
                if film.title == doc["_source"]["title"]:
                    break
            else:
                person_films.append(FilmWorkOut(**doc["_source"]))

        return person_films

    async def get_person_detail(self, person_id: str,
                                role: str) -> Optional[PersonOut]:
        """
        Возвращает данные по конкретной персоне
        role=... указывает с какой ролью этой персоны делать запрос,
        """
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
        """
        Производит поиск по персонам -
        query=... для поиска по персоне,
        role=... для указания с какой ролью этой персоны делать запрос,
        page=1&page_size=10 - для выбора страницы и количества записей на странице
        """
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
                query={"query": {"match": {"full_name": query}}},
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
