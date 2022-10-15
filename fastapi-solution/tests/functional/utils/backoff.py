import logging
import time
from functools import wraps
from logging import Logger

import elasticsearch
import redis

logger = logging.getLogger(__name__)


def backoff(
    start_sleep_time: float = 0.1,
    factor: int = 2,
    border_sleep_time: int = 25,
    connection_attempts: int = 20,
    log: Logger = logger,
):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора
    (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param connection_attempts: кол-во попыток соединиться
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :param log: логер
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        connect_timer = start_sleep_time

        @wraps(func)
        async def inner(**kwargs):
            nonlocal connect_timer
            try_ = 0
            while try_ != connection_attempts:
                time.sleep(connect_timer)
                try:
                    result = await func(**kwargs)
                    connect_timer = 0.1
                    return result
                except elasticsearch.exceptions.ConnectionError:
                    log.warning(
                        f"Elasticsearch соединение потеряно, следующая попытка соединения {connect_timer} sec "
                        f"Осталось попыток {connection_attempts - try_}"
                    )
                    connect_timer = connect_timer * 2**factor
                    try_ += 1
                    if connect_timer > border_sleep_time:
                        connect_timer = start_sleep_time
                except redis.exceptions.ConnectionError:
                    log.warning(
                        f"redis соединение потеряно, следующая попытка соединения {connect_timer} sec "
                        f"Осталось попыток {connection_attempts - try_}"
                    )
                    connect_timer = connect_timer * 2**factor
                    try_ += 1
                    if connect_timer > border_sleep_time:
                        connect_timer = start_sleep_time

        return inner

    return func_wrapper
