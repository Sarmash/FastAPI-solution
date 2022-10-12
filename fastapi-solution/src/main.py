import aioredis
from api.v1 import films, genres, persons
from core.backoff import backoff
from core.config import default_settings
from db import elastic, redis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title=default_settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
@backoff()
async def startup():
    redis.redis = await aioredis.create_redis_pool(
        (default_settings.redis_host, default_settings.redis_port),
        minsize=10,
        maxsize=20,
    )
    elastic.es = AsyncElasticsearch(hosts=[default_settings.elasticsearch_connect])


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])
