from models.base_model import BasicModel


class FilmWork(BasicModel):
    id: str
    title: str
    imdb_rating: float = 0.0
    description: str = None
    genre: list = []
    actors: list = []
    writers: list = []
    directors: list = []
