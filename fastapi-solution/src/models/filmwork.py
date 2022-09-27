import orjson
from functions_for_models import orjson_dumps
from pydantic import BaseModel


class FilmWork(BaseModel):
    id: str
    title: str
    imdb_rating: float = 0.0
    description: str = None
    genre: list = []
    actors: list = []
    writers: list = []
    directors: list = []

    class Config:
        # Заменяем стандартную работу с json на более быструю.
        json_loads = orjson.loads
        json_dumps = orjson_dumps
