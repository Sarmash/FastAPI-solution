import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    """orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декорируем"""

    return orjson.dumps(v, default=default).decode()


class BasicModel(BaseModel):
    """Родительская модель с orjson"""

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
