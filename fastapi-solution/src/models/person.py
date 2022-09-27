from models.base_model import BasicModel


class Person(BasicModel):
    id: str
    film_work: list = []
    role: list = []
