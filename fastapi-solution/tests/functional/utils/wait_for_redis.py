import asyncio

from backoff import backoff

from aioredis import Redis


@backoff()
async def wait_for_redis():
    redis_client = Redis("redis://localhost")
    if not redis_client:
        raise ConnectionRefusedError


if __name__ == "__main__":
    asyncio.run(wait_for_redis())
