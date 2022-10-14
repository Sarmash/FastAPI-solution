import asyncio

import aiohttp
import pytest
import pytest_asyncio
from aioredis import create_connection
from elasticsearch import AsyncElasticsearch

from .settings import test_settings

pytest_plugins = (
    f"{test_settings.container}.fixtures.filling_elastic_fixtures",
    f"{test_settings.container}.fixtures.redis_fixtures",
)


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
