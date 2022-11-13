import enum
from functools import wraps
from http import HTTPStatus
import core.http_exceptions as ex
from fastapi import HTTPException

from core.jwt_api import decode_jwt, token_time_exited


class Permissions(enum.Enum):
    """Уровни доступа фильмов,
    каждому уровню соответствует число для определения доступа"""
    All = "all"
    All_value = 1
    User = "user"
    User_value = 2
    Subscriber = "subscriber"
    Subscriber_value = 3

    @classmethod
    def get_permission_value(cls, permission: str):
        permission = permission.lower()
        if permission == cls.All.value:
            return 1
        if permission == cls.User.value:
            return 2
        if permission == cls.Subscriber.value:
            return 3


def permissions(permission: Permissions = Permissions.All):
    """Декоратор доступа к ендпоинтам по токену,
    принмиает Permission объект для установки
    определенного доступа к ендпоинту.
    Требует обязательного параметра token
    у ендпоинта для перехвата токена клиента."""
    def film_permissions(f):

        @wraps(f)
        async def decorator(*args, **kwargs):
            token = kwargs.get("token")
            if token:
                token = token.credentials
                token_data = decode_jwt(token)
                if not token_data:
                    if permission == Permissions.All:
                        return await f(*args, **kwargs)
                if token_time_exited(token_data):
                    raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED,
                                        detail=ex.TOKEN_OUTDATED)
                else:
                    user_permission = Permissions.get_permission_value(
                        token_data.get("role"))
                    if user_permission >= Permissions.get_permission_value(
                        permission.value
                    ):
                        return await f(*args, **kwargs)
                    raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
                                        detail=ex.WRONG_PERMISSION)
            elif permission == permission.All:
                return await f(*args, **kwargs)
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN,
                                detail=ex.WRONG_PERMISSION)
        return decorator
    return film_permissions
