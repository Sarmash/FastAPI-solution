from models.base_model import BasicModel


class Genre(BasicModel):
    """Модель для формирования и ответа по запросу жанров"""

    id: str
    genre: str
