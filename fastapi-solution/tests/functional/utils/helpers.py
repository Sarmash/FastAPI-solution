import json
from typing import Union

from elasticsearch import AsyncElasticsearch
from aioredis import RedisConnection


async def elastic_search_list(
        client: AsyncElasticsearch,
        index: str,
        size: int = 50) -> list[dict]:
    """Запрос в еластик на получение списка данных"""

    response_elastic = await client.search(index=index, size=size)
    response_elastic = response_elastic['hits']['hits']
    return [item['_source'] for item in response_elastic]


async def elastic_search_by_id(
        client: AsyncElasticsearch,
        index: str,
        id_: str) -> dict:
    """Запрос в еластик на получение данных по id"""

    response_elastic = await client.get(index=index, id=id_)
    return response_elastic["_source"]


async def redis_get(client: RedisConnection,
                    key: str) -> Union[list[dict], dict]:
    """Запрос в редис на получение данных по ключу"""

    response = await client.execute("GET", key)
    assert isinstance(response, bytes)
    response = json.loads(response)
    if isinstance(response, list):
        return [json.loads(i) for i in response]
    else:
        return response
