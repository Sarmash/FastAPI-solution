import json
import uuid

import aiohttp
import pytest
from elasticsearch import AsyncElasticsearch

from ..settings import test_settings


@pytest.mark.asyncio
async def test_search():
    es_data = [
        {
            "id": str(uuid.uuid4()),
            "imdb_rating": 8.5,
            "genre": ["Action", "Sci-Fi"],
            "title": "The Star",
            "description": "New World",
            "director": "Stan",
            "actors_names": ["Ann", "Bob"],
            "writers_names": ["Ben", "Howard"],
            "actors": [
                {"id": "111", "name": "Ann"},
                {"id": "222", "name": "Bob"},
            ],
            "writers": [{"id": "333", "name": "Ben"}, {"id": "444", "name": "Howard"}],
        }
        for _ in range(60)
    ]

    bulk_query = []
    for row in es_data:
        id = row[test_settings.es_id_field]
        bulk_query.extend(
            [
                json.dumps({"index": {"_index": test_settings.es_index, "_id": id}}),
                json.dumps(row),
            ]
        )

    str_query = "\n".join(bulk_query) + "\n"

    es_client = AsyncElasticsearch(
        hosts=test_settings.es_host,
        validate_cerl=False,
        use_ssl=False,
    )
    response = await es_client.bulk(str_query, refresh=True)
    await es_client.close()
    if response["errors"]:
        raise Exception("Ошибка записи данных в Elasticsearch")

    session = aiohttp.ClientSession()
    url = test_settings.service_url + "films/"
    query_data = {"sort": "-imdb_rating", "page[size]": 50, "page[number]": 1}
    async with session.get(url, params=query_data) as response:
        body = await response.json()
        # headers = response.json()
        status = response.status
    await session.close()

    assert status == 200
    assert len(body) == 50
