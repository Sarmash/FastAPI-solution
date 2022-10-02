from http import HTTPStatus

from db.redis import cache
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from models.person import PersonOut, FilmWorkOut
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get(path="/{person_id}/film/",)
@cache
async def person_film_list(
        request: Request,
        person_id: str,
        service: PersonService = Depends(get_person_service)
) -> list[FilmWorkOut]:
    """
    Эндпоинт - /api/v1/persons/{person_id}/film/ - возвращает
    список фильмов, в которых участвовал конкретный человек
    """
    list_person = await service.get_person_film_list(person_id)
    if not list_person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='page not found'
        )
    return list_person


@router.get('/search/')
async def search_person(
        query: str,
        service: PersonService = Depends(get_person_service),
        page: int = Query(default=1, gt=0),
        page_size: int = Query(default=50, gt=0)
) -> list[PersonOut]:
    """
    Эндпоинт - /api/v1/persons/search/ - возвращает поиск по персонам
    - /api/v1/persons/search/?query=...&role=...page=1&page_size=10 -
    query=... для поиска по персоне,
    role=... для указания с какой ролью этой персоны делать запрос,
    page=1&page_size=10 - для выбора страницы и количества записей на странице
    """
    list_person = await service.search_person(query, page_size, page)
    if not list_person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='page not found'
        )
    return list_person


@router.get('/{person_id}/')
@cache
async def person_details(request: Request, person_id: str,
                         role: str = Query(default='actors'),
                         service: PersonService = Depends(
                             get_person_service
                         )) -> list[PersonOut]:
    """
    Эндпоинт - /api/v1/persons/{person_id}/ - возвращает данные по
    конкретной персоне
    - /api/v1/persons/search/?role=...-
    role=... указывает с какой ролью этой персоны делать запрос,
    """
    person = await service.get_person_detail(person_id, role)
    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='person not found'
        )
    return person
