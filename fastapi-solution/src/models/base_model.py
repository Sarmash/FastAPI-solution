import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декорируем.
    return orjson.dumps(v, default=default).decode()


class BasicModel(BaseModel):
    class Config:
        # Заменяем стандартную работу с json на более быструю.
        json_loads = orjson.loads
        json_dumps = orjson_dumps
