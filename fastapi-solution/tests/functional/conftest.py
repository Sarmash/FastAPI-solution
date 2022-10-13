import asyncio
import json
from typing import List

import aiohttp
import pytest
import pytest_asyncio
from aioredis import RedisConnection, create_connection
from elasticsearch import AsyncElasticsearch

from .testdata.data import GENRES, MOVIES, PERSONS
from .settings import test_settings
from .utils.helpers import elastic_filling_index, get_es_bulk_query, elastic_delete_data


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
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(data: List[dict], index: str):
        bulk_query = get_es_bulk_query(data, index, test_settings.movies_id_field)
        str_query = "\n".join(bulk_query) + "\n"
        response = await es_client.bulk(str_query, refresh=True)
        if response["errors"]:
            raise Exception("Ошибка записи данных в Elasticsearch")

    return inner


@pytest_asyncio.fixture(scope="function")
async def es_write_genre(es_client: AsyncElasticsearch):
    await elastic_filling_index(es_client, test_settings.genres_index, GENRES)
    yield
    await elastic_delete_data(es_client, test_settings.genres_index)


@pytest_asyncio.fixture(scope="function")
async def es_write_movies(es_client: AsyncElasticsearch):
    await elastic_filling_index(es_client, test_settings.movies_index, MOVIES)
    yield
    await elastic_delete_data(es_client, test_settings.movies_index)


@pytest_asyncio.fixture(scope="function")
async def es_write_persons(es_client: AsyncElasticsearch):
    await elastic_filling_index(es_client, test_settings.persons_index, PERSONS)
    yield
    await elastic_delete_data(es_client, test_settings.persons_index)


@pytest.fixture
def es_delete_data(es_client: AsyncElasticsearch):
    async def inner(indexes: tuple):
        for index in indexes:
            await es_client.delete_by_query(
                conflicts="proceed", index=index, body={"query": {"match_all": {}}}
            )

    return inner


@pytest.fixture
def make_get_request(session_client: aiohttp.ClientSession):
    async def session(url: str, query_data: dict):
        response = await session_client.get(url, params=query_data)

        return response

    return session


@pytest.fixture
def make_get_request_url(session_client: aiohttp.ClientSession):
    async def session(url):
        response = await session_client.get(url)

        return response

    return session


@pytest.fixture
def elastic_search_list_fixture(es_client: AsyncElasticsearch):
    async def inner(index: str, id: str = None, size: int = 50):
        if id:
            response_elastic = await es_client.get(index=index, id=id)
            return response_elastic["_source"]
        else:
            response_elastic = await es_client.search(index=index, size=size)
            response_elastic = response_elastic["hits"]["hits"]
            return [item["_source"] for item in response_elastic]

    return inner


@pytest.fixture
def redis_get_fixture(redis_client: RedisConnection):
    async def inner(key: str):
        response = await redis_client.execute("GET", key)
        response = json.loads(response)
        if isinstance(response, list):
            return [json.loads(i) for i in response]
        else:
            return response

    return inner


@pytest.fixture
def redis_delete_fixture(redis_client: RedisConnection):
    async def inner(key: str):
        await redis_client.execute("DEL", key)

    return inner
