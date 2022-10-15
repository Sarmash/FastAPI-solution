import json
from typing import List, Union

from aiohttp import ClientSession
from aioredis import RedisConnection
from elasticsearch import AsyncElasticsearch


async def elastic_search_list(
    client: AsyncElasticsearch, index: str, size: int = 50, body: dict = None
) -> List[dict]:
    """Запрос в еластик на получение списка данных"""

    response_elastic = await client.search(index=index, size=size, body=body)
    response_elastic = response_elastic["hits"]["hits"]
    return [item["_source"] for item in response_elastic]


async def elastic_search_by_id(
    client: AsyncElasticsearch, index: str, id_: str
) -> dict:
    """Запрос в еластик на получение данных по id"""

    response_elastic = await client.get(index=index, id=id_)
    return response_elastic["_source"]


async def redis_get(client: RedisConnection, key: str) -> Union[List[dict], dict]:
    """Запрос в редис на получение данных по ключу"""

    response = await client.execute("GET", key)
    assert isinstance(response, bytes)
    response = json.loads(response)
    if isinstance(response, list):
        return [json.loads(i) for i in response]
    else:
        return response


async def http_request(client: ClientSession, request: str, status_code: int) -> dict:
    """GET запрос с переводом в json"""

    response_api = await client.get(request)
    assert response_api.status == status_code
    return await response_api.json()


def get_es_bulk_query(data: List[dict], index: str, id: str):
    """Форматирование данных для записи в elasticsearch через bulk"""

    bulk_query = []
    for row in data:
        bulk_query.extend(
            [json.dumps({"index": {"_index": index, "_id": row[id]}}), json.dumps(row)]
        )

    return bulk_query


async def elastic_filling_index(
    client: AsyncElasticsearch, index: str, data: List[dict]
):
    """Заполнение индекса elasticsearch данными"""

    bulk_query = get_es_bulk_query(data, index, "id")
    str_query = "\n".join(bulk_query) + "\n"
    response = await client.bulk(str_query, refresh=True)
    if response["errors"]:
        raise Exception("Ошибка записи данных в Elasticsearch")


async def elastic_delete_data(client: AsyncElasticsearch, index: str):
    """Очистка индекса elasticsearch от всех данных"""

    await client.delete_by_query(
        conflicts="proceed",
        index=index,
        body={"query": {"match_all": {}}},
    )
