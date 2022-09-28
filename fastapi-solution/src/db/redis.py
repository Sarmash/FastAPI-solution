import json
from functools import wraps
from typing import Optional

from aioredis import Redis
from core.config import FILM_CACHE_EXPIRE_IN_SECONDS

redis: Optional[Redis] = None


# Функция понадобится при внедрении зависимостей.
async def get_redis() -> Redis:
    return redis


def cache(func):
    """Декоратор для кеширования в редис, ключ - URL запроса,
    для корректной работы декоратора в параметрах функции ендпоинта,
    должен быть fastapi Request"""

    @wraps(func)
    async def inner(**kwargs):
        request = str(kwargs['request'].url)
        redis_client = kwargs['film_service'].redis

        data = await redis_client.get(request)
        if data is not None:
            return json.loads(data)

        result_for_cache = result = await func(**kwargs)

        if isinstance(result, list) is not True:
            result_for_cache = result.json()
        else:
            result_for_cache = json.dumps(result_for_cache)

        await redis_client.set(key=request,
                               value=result_for_cache,
                               expire=FILM_CACHE_EXPIRE_IN_SECONDS)
        return result

    return inner
