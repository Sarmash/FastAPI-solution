import asyncio

import redis
from backoff import backoff


@backoff()
async def wait_for_redis():
    redis_client = redis.Redis(host="redis", port=6379, db=0)
    if not redis_client.ping():
        raise redis.exceptions.ConnectionError


if __name__ == "__main__":
    asyncio.run(wait_for_redis())
