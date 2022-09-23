import logging

import aioredis
import uvicorn
from api.v1 import films
from core import config
from core.logger import LOGGING
from db import elastic, redis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    # Конфигурируем название проекта. Оно будет отображаться в документации.
    title=config.PROJECT_NAME,
    # Адрес документации в красивом интерфейсе.
    docs_url="/api/openapi",  # Адрес документации в формате OpenAPI.
    openapi_url="/api/openapi.json",
    # Замена стандартного JSON-сереализатора на версию, написанную на Rust.
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    # Подключаемся к базам при старте сервера
    redis.redis = await aioredis.create_redis_pool(
        (config.REDIS_HOST, config.REDIS_PORT), minsize=10, maxsize=20
    )
    elastic.es = AsyncElasticsearch(
        hosts=[f"{config.ELASTIC_HOST}:{config.ELASTIC_PORT}"]
    )


@app.on_event("shutdown")
async def shutdown():
    # Отключаемся от баз при выключенном сервере.
    await redis.redis.close()
    await elastic.es.close()


# Подключаем роутер к серверу, указав префикс /v1/films
app.include_router(films.router, prefix="/api/v1/films", tags=["films"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
