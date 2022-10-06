from http import HTTPStatus
from typing import List, Optional

import core.http_exceptions as ex
from db.redis import Cache
from fastapi import APIRouter, Depends, HTTPException, Request
from services.person import PersonService, get_person_service
from services.service_base import Paginator

router = APIRouter()


@router.get(
    "/{person_id}/film/",
    summary="Возвращает список фильмов, в которых участвует персона",
    description="Возвращает список фильмов, в которых участвует персона (uuid, название и рейтинг)",
)
@Cache()
async def person_list(
    request: Request,
    person_id: str,
    service: PersonService = Depends(get_person_service),
) -> list:
    """Эндпоинт - /api/v1/persons/<uuid:UUID>/film/ - возвращающий список, в которых участвовала персона"""
    list_person = await service.person_films(person_id)
    if not list_person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ex.FILM_NOT_FOUND)
    return list_person


@router.get(
    "/search",
    summary="Производит поиск по персонам",
    description="Возвращает uuid, имя, роль и фильмы искомой персоны. "
                "Принимает параметр query, по которому произваодится поиск"
)
@Cache()
async def search_person(
    request: Request,
    query: str,
    service: PersonService = Depends(get_person_service),
    paginator: Paginator = Depends(),
) -> list:
    """Эндпроинт - /api/v1/persons/search/?query=George&page=1&page_size=10 -
    возвращающий список совпадений по квери"""

    list_person = await service.search_person(
        query, paginator.page_size, paginator.page_number
    )
    if not list_person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ex.PAGE_NOT_FOUND)
    return list_person


@router.get(
    "/{person_id}/",
    summary="Возвращает данные по конкретной персоне",
    description="Возвращает данные по конкретной персоне: его uuid, имя, роль"
                "и фильмы, в которых он(а) принимал(а) участие",
)
@Cache()
async def person_details(
    request: Request,
    person_id: str,
    service: PersonService = Depends(get_person_service),
) -> Optional[List]:
    """Эндпоинт - /api/v1/persons/a5a8f573-3cee-4ccc-8a2b-91cb9f55250a/ -
    для вывода списка фильмов по ролям в которых участвовал человек"""

    person = await service.get_person_detail(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ex.PERSON_NOT_FOUND)
    return person
