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


class FilmWorkOut(BasicModel):
    """Модель ответа для клиента по запросу о фильмах"""

    id: str
    title: str
    imdb_rating: Optional[float]
