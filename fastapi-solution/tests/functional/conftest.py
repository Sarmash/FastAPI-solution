import asyncio
import json
from typing import List

import aiohttp
import pytest
import pytest_asyncio
from aioredis import create_connection
from elasticsearch import AsyncElasticsearch

from .base_function import get_es_bulk_query
from .settings import test_settings


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def redis_client():
    client = await create_connection(
        (test_settings.redis_host, test_settings.redis_port)
    )
    yield client
    client.close()


@pytest_asyncio.fixture(scope="session")
async def es_client():
    client = AsyncElasticsearch(hosts=test_settings.es_host)
    yield client
    await client.close()


@pytest_asyncio.fixture(scope="session")
async def session_client():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def es_write_data(es_client):
    async def inner(data: List[dict]):
        bulk_query = get_es_bulk_query(
            data, test_settings.movies_index, test_settings.movies_id_field
        )
        str_query = "\n".join(bulk_query) + "\n"

        response = await es_client.bulk(str_query, refresh=True)
        if response["errors"]:
            raise Exception("Ошибка записи данных в Elasticsearch")

    return inner


@pytest.fixture
def es_write_persons(es_client):
    async def gen_data_persons(es_data_persons: List[dict]):
        bulk_query_perons = []
        for row in es_data_persons:
            bulk_query_perons.extend(
                [
                    json.dumps(
                        {
                            "index": {
                                "_index": test_settings.persons_index,
                                "_id": row[test_settings.persons_id_field],
                            }
                        }
                    ),
                    json.dumps(row),
                ]
            )
        str_query = "\n".join(bulk_query_perons) + "\n"
        response = await es_client.bulk(str_query, refresh=True)
        if response["errors"]:
            raise Exception("Ошибка записи данных в Elasticsearch")

    return gen_data_persons


@pytest.fixture
def make_get_request(session_client: aiohttp.ClientSession):
    async def session(url: str, query_data: dict):
        url_address = test_settings.service_url + url
        response = await session_client.get(url_address, params=query_data)

        return response

    return session
