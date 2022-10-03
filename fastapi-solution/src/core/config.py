import os
from logging import config as logging_config

from core.logger import LOGGING
from pydantic import BaseSettings

logging_config.dictConfig(LOGGING)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    project_name: str = os.getenv("PROJECT_NAME", "movies")

    elasticsearch_connect: str = os.environ.get("ELASTICSEARCH", 'http://localhost:9200')
    redis_host: str = os.getenv("REDIS_HOST", "127.0.0.1")
    redis_port: int = int(os.getenv("REDIS_PORT", 6379))
    redis_cache_expire_in_seconds: int = 60 * 3


default_settings = Settings()
