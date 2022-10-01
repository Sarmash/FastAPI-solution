from uuid import UUID

from models.base_model import BasicModel

from typing import Optional


class Person(BasicModel):
    id: str
    full_name: str
    # roles: str
    # film_ids: Optional[list[UUID]] = []
    # film_ids: str
