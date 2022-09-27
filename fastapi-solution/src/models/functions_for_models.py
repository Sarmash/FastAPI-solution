import orjson


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декорируем.
    return orjson.dumps(v, default=default).decode()
