from typing import Optional

from models.base_model import BasicModel


class FilmWork(BasicModel):
    """Модель формирования filmwork из elasticsearch"""

    id: str
    title: str
    imdb_rating: Optional[float]
    description: Optional[str]
    genre: list = []
    actors: list = []
    writers: list = []
    director: Optional[str]
    permission: Optional[str]


class FilmWorkOut(BasicModel):
    """Модель ответа для клиента по запросу о фильмах"""

    id: str
    title: str
    imdb_rating: Optional[float]


class Forbidden(BasicModel):
    """Модель ответа для клиента без доступа к запрашиваемому фильму"""

    response: str

    class Config:
        schema_extra = {
            "example": {
                "response": "wrong permission user"
            }
        }


class Unauthorized(Forbidden):
    """Модель ответа для клиента с истекшим временем токена"""

    class Config:
        schema_extra = {
            "example": {
                "response": "token outdated"
            }
        }
