import json
from functools import wraps
from typing import Optional

from aioredis import Redis
from core.config import default_settings

redis: Optional[Redis] = None


async def get_redis() -> Redis:
    return redis


def cache(func):
    """Декоратор для кеширования в редис,
    в качестве ключа используется имя функции и её параметры"""

    @wraps(func)
    async def inner(**kwargs):
        key = f"{func.__name__}/{kwargs}"
        redis_client = kwargs["service"].redis

        data = await redis_client.get(key)
        if data is not None:
            data_from_redis = json.loads(data)
            if isinstance(data_from_redis, list):
                data_for_return = [json.loads(model) for model in data_from_redis]
            else:
                data_for_return = json.loads(data)
            return data_for_return

        result_for_cache = result = await func(**kwargs)

        if isinstance(result, list) is not True:
            result_for_cache = result.json()
        else:
            result_for_cache = json.dumps([model.json() for model in result_for_cache])

        await redis_client.set(
            key=key, value=result_for_cache, expire=default_settings.redis_cache_expire_in_seconds
        )
        return result

    return inner
