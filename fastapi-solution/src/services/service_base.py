from http import HTTPStatus

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import HTTPException, Query


class Service:
    """Родительский класс для сервисов"""

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic


class Paginator:
    def __init__(
        self,
        page_size: int = Query(
            ge=0,
            le=100,
            default=50,
            alias="page[size]",
            description="Items amount on page",
        ),
        page_number: int = Query(
            default=1,
            ge=1,
            alias="page[number]",
            description="Page number for pagination",
        ),
    ):
        self.page_size = page_size
        self.page_number = page_number

    def pagination(self, films: list) -> list:
        """Пагинатор"""
        first_number = (self.page_number - 1) * self.page_size
        if first_number >= len(films) or len(films) == 0:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="page not found"
            )
        second_number = first_number + self.page_size
        return films[first_number:second_number]


class Filter:
    def __init__(
        self,
        filter_query: str = Query(
            default=None,
            alias="filter[genre]",
            description="Genre id",
        ),
    ):
        self.genre_id = filter_query
