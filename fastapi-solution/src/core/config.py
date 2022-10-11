import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings, Field

logging_config.dictConfig(LOGGING)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    project_name: str = "movies"

    elasticsearch_connect: str = Field("http://localhost:9200", env="ELASTICSEARCH")
    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: int = Field(..., env="REDIS_PORT")

    redis_cache_expire_in_seconds: int = 60 * 3


default_settings = Settings()
