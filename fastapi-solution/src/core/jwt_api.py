import datetime

from jwt import decode
from core.config import default_settings
from models.token import TokenRequest


def decode_jwt(token: str):
    try:
        TokenRequest(Authorization=token)
    except:
        return
    token = token.split(' ')
    payload = decode(token[1], key=default_settings.jwt_key, algorithms="HS256")
    end_time = payload["end_time"]
    end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S.%f")
    time_for_exited = (
        end_time.timestamp() - datetime.datetime.utcnow().timestamp()
    )
    if time_for_exited <= 0:
        return
    return payload
