import orjson
from models.functions_for_models import orjson_dumps
from pydantic import BaseModel


class Genre(BaseModel):
    id: str
    genre_name: str

    class Config:
        # Заменяем стандартную работу с json на более быструю.
        json_loads = orjson.loads
        json_dumps = orjson_dumps
