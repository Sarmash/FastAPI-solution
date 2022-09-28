from aioredis import Redis
from elasticsearch import AsyncElasticsearch


class Service:
    """Родительский класс для сервисов"""

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
