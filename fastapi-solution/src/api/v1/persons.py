from http import HTTPStatus

from db.redis import cache
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from models.person import Person
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get('/')
@cache
async def person_list(
        request: Request,
        service: PersonService = Depends(get_person_service),
        page: int = Query(default=1, gt=0),
        page_size: int = Query(default=50, gt=0)
) -> list[Person]:
    list_person = await service.get_person_list(page_size, page)
    if not list_person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='page not found'
        )
    return list_person


@router.get('/{person_id}', response_model=Person)
@cache
async def person_details(request: Request, person_id: str,
                         service: PersonService = Depends(
                             get_person_service
                         )) -> list[Person]:

    person = await service.get_person_detail(person_id)

    if not person:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='person not found'
        )

    return person
