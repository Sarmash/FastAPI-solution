from http import HTTPStatus

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import HTTPException


class Service:
    """Родительский класс для сервисов"""

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    @staticmethod
    def pagination(films: list, page_size: int, page_number: int) -> list:
        """Пагинатор"""
        first_number = (page_number - 1) * page_size
        if first_number >= len(films) or len(films) == 0:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="page not found"
            )
        second_number = first_number + page_size
        return films[first_number:second_number]
