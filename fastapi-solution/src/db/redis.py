import json
from functools import wraps
from typing import Optional, Union
from pydantic import BaseModel
from aioredis import Redis
from core.config import default_settings
from core.logger import logger

redis: Optional[Redis] = None


async def get_redis() -> Redis:
    return redis


class Cache:

    @staticmethod
    def _deserializing_received_data(data: bytes) -> Union[list, dict]:

        data_from_redis = json.loads(data)
        if isinstance(data_from_redis, list):
            data_for_return = [json.loads(model) for model in data_from_redis]
        else:
            data_for_return = json.loads(data)

        return data_for_return

    @staticmethod
    def _serializing_data_for_set_in_redis(data: Union[list, BaseModel]) -> bytes:

        if isinstance(data, list) is not True:
            result_for_cache = data.json()
        else:
            result_for_cache = json.dumps([model.json() for model in data])

        return result_for_cache.encode()

    def __call__(self, func):
        """Декоратор для кеширования в редис, ключ - URL запроса.
            Для корректной работы декоратора в параметрах функции ендпоинта,
            должен быть fastapi Request
            def endpoint(some_parameters, request: Request)
                some logic
                return some_result
            """

        @wraps(func)
        async def inner(**kwargs):
            request = kwargs.get("request")
            if request is None:
                logger.warn("Декоратор кеширования не работает, отсутствует переменная request")
                return await func(**kwargs)

            request = str(request.url)
            redis_client = kwargs["service"].redis

            data = await redis_client.get(request)
            if data is not None:
                return self._deserializing_received_data(data)

            result = await func(**kwargs)

            result_for_cache = self._serializing_data_for_set_in_redis(result)

            await redis_client.set(
                key=request,
                value=result_for_cache,
                expire=default_settings.redis_cache_expire_in_seconds,
            )
            return result

        return inner
