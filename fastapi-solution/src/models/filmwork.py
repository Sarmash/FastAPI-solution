from typing import Optional

from models.base_model import BasicModel


class FilmWork(BasicModel):
    """Модель формирования filmwork из elasticsearch"""

    id: str
    title: str
    imdb_rating: Optional[float]
    description: Optional[str] = None
    genre: list = []
    actors: list = []
    writers: list = []
    directors: Optional[str] = None


class FilmWorkOut(BasicModel):
    """Модель ответа для клиента по запросу о фильмах"""

    id: str
    title: str
    imdb_rating: Optional[float]
