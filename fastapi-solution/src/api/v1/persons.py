from http import HTTPStatus
from typing import List, Optional

import core.http_exceptions as ex
from db.redis import cache
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get("/{person_id}/film/")
@cache
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


@router.get("/search/")
@cache
async def search_person(
    request: Request,
    query: str,
    service: PersonService = Depends(get_person_service),
    page: int = Query(default=1, gt=0),
    page_size: int = Query(default=50, gt=0),
) -> list:
    """Эндпроинт - /api/v1/persons/search/?query=George&page=1&page_size=10 -
    возвращающий список совпадений по квери"""

    list_person = await service.search_person(query, page_size, page)
    if not list_person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ex.PAGE_NOT_FOUND)
    return list_person


@router.get("/{person_id}/")
@cache
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
