import pytest
from aioredis import RedisConnection


@pytest.fixture
def redis_delete_fixture(redis_client: RedisConnection):
    """Фикстура для очистки данных в редис по ключу"""

    async def inner():
        await redis_client.execute("FLUSHDB")

    return inner
