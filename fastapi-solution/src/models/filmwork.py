import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декорируем.
    return orjson.dumps(v, default=default).decode()


class FilmWork(BaseModel):
    id: str
    title: str
    imdb_rating: float = 0.0
    description: str
    genre: list = []
    actors: list = []
    writers: list = []
    directors: list = []

    class Config:
        # Заменяем стандартную работу с json на более быструю.
        json_loads = orjson.loads
        json_dumps = orjson_dumps
