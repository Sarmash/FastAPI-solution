from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    container: str = Field("functional", env="CONTAINER")
    es_host: str = Field("http://localhost:9200/", env="ELASTICSEARCH")

    movies_index: str = "movies"
    movies_endpoint: str = "films/"
    movies_id_field: str = "id"

    redis_host: str = Field("localhost", env="REDIS_HOST")
    redis_port: str = Field(6379, env="REDIS_PORT")

    service_url: str = Field("http://localhost:8000/api/v1/", env="SERVICE_URL")

    genres_index: str = "genres"
    genres_endpoint: str = "genres/"

    persons_index: str = "persons"
    persons_id_field: str = "id"
    persons_endpoint: str = "persons/"

    search_persons_endpoint: str = "persons/search"
    search_films_endpoint: str = "films/search/"


test_settings = TestSettings()
