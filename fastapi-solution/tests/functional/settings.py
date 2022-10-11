from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    es_host: str = Field("http://elasticsearch:9200/", env="ELASTIC_HOST")

    movies_index: str = "movies"
    movies_id_field: str = "id"

    redis_host: str = Field("redis", env="REDIS_HOST")
    redis_port: str = Field(6379, env="REDIS_PORT")

    service_url: str = "http://fastapi:8000/api/v1/"

    genres_index: str = "genres"
    genres_endpoint: str = "genres/"

    persons_index: str = "persons"
    persons_id_field: str = "id"
    persons_endpoint: str = "persons/"


test_settings = TestSettings()
