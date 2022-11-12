import datetime
from typing import Optional

import pydantic
from jwt import decode
from core.config import default_settings
from models.token import TokenRequest


def decode_jwt(token: str) -> Optional[dict]:
    """Получение данных из токена"""
    try:
        TokenRequest(Authorization=token)
    except pydantic.error_wrappers.ValidationError:
        return
    token = token.split(' ')
    return decode(token[1], key=default_settings.jwt_key, algorithms="HS256")


def token_time_exited(payload: dict) -> bool:
    end_time = payload["end_time"]
    end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f")
    time_for_exited = (
            end_time.timestamp() - datetime.datetime.utcnow().timestamp()
    )
    if time_for_exited <= 0:
        return True
    return False
