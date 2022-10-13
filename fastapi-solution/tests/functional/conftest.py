import asyncio

import aiohttp
import pytest
import pytest_asyncio
from aioredis import RedisConnection, create_connection
from elasticsearch import AsyncElasticsearch

from .testdata.data import GENRES, MOVIES, PERSONS
from .settings import test_settings
from .utils.helpers import elastic_filling_index, elastic_delete_data


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def redis_client():
    """Создание подключения к редис"""
    client = await create_connection(
        (test_settings.redis_host, test_settings.redis_port)
    )
    yield client
    client.close()


@pytest_asyncio.fixture(scope="session")
async def es_client():
    """Создание подключения к elasticsearch"""
    client = AsyncElasticsearch(hosts=test_settings.es_host)
    yield client
    await client.close()


@pytest_asyncio.fixture(scope="session")
async def session_client():
    """Создание http сессии"""
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(scope="function")
async def es_write_genre(es_client: AsyncElasticsearch):
    """Фикстура для записи и удаления данных из индекса жанров в elasticsearch"""
    await elastic_filling_index(es_client, test_settings.genres_index, GENRES)
    yield
    await elastic_delete_data(es_client, test_settings.genres_index)


@pytest_asyncio.fixture(scope="function")
async def es_write_movies(es_client: AsyncElasticsearch):
    """Фикстура для записи и удаления данных из индекса кинопроизведений в elasticsearch"""
    await elastic_filling_index(es_client, test_settings.movies_index, MOVIES)
    yield
    await elastic_delete_data(es_client, test_settings.movies_index)


@pytest_asyncio.fixture(scope="function")
async def es_write_persons(es_client: AsyncElasticsearch):
    """Фикстура для записи и удаления данных из индекса персон в elasticsearch"""
    await elastic_filling_index(es_client, test_settings.persons_index, PERSONS)
    yield
    await elastic_delete_data(es_client, test_settings.persons_index)


@pytest.fixture
def redis_delete_fixture(redis_client: RedisConnection):
    """Фикстура для очистки данных в редис по ключу"""

    async def inner():
        await redis_client.execute("FLUSHDB")

    return inner
