from http import HTTPStatus

from db.redis import cache
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from models.person import PersonOut
from services.person import PersonService, get_person_service

router = APIRouter()


@router.get("/{person_id}/film")
async def person_list(
    query: str = Query(
        default="bccbbbb6-be40-44f5-a025-204bcfcf2667", description="Persons id"
    ),
    service: PersonService = Depends(get_person_service),
    page: int = Query(default=1, gt=0),
    page_size: int = Query(default=50, gt=0),
) -> list:
    list_person = await service.person_films(query, page_size, page)
    if not list_person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return list_person


@router.get("/search/")
async def search_person(
    query: str,
    role: str = Query(default="actors"),
    service: PersonService = Depends(get_person_service),
    page: int = Query(default=1, gt=0),
    page_size: int = Query(default=50, gt=0),
) -> list[PersonOut]:
    list_person = await service.search_person(query, role, page_size, page)
    if not list_person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="page not found")
    return list_person


@router.get("/{person_id}/")
@cache
async def person_details(
    request: Request,
    person_id: str,
    role: str = Query(default="actors"),
    service: PersonService = Depends(get_person_service),
) -> list:
    person = await service.get_person_detail(person_id, role)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="person not found")
    return person
