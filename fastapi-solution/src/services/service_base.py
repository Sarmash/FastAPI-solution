from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from typing import Generator


class Service:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def scroll(self, index: str, scroll: str, size: int, **kw) -> Generator:
        """Генератор для запросов к elasticsearch с помощью scroll
        для возвращения результата постранично"""

        page = await self.elastic.search(index=index, scroll=scroll,
                                         size=size, **kw)
        scroll_id = page['_scroll_id']
        hits = page['hits']['hits']

        while len(hits):
            yield hits
            page = await self.elastic.scroll(scroll_id=scroll_id, scroll=scroll)
            scroll_id = page['_scroll_id']
            hits = page['hits']['hits']
