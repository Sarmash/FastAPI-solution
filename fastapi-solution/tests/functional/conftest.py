import asyncio

from pytest import fixture
from aiohttp import ClientSession
from elasticsearch import AsyncElasticsearch
from aioredis import create_redis_pool


@fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@fixture(scope='session')
async def http_client():
    session = ClientSession()
    yield session
    await session.close()


@fixture(scope="session")
async def elastic_client():
    client = AsyncElasticsearch(hosts=['http://elasticsearch:9200'])
    yield client
    await client.close()


@fixture(scope="session")
async def redis_client():
    client = await create_redis_pool(
        ('redis', 6379)
    )
    yield client
    client.close()
