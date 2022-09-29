from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from models.filmwork import FilmWork
from services.filmwork import FilmService, get_film_service

router = APIRouter()


@router.get("/{film_id}", response_model=FilmWork)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> FilmWork:
    """Эндпоинт - /api/v1/films/{film_id} - возвращающий данные по фильму"""
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return film


@router.get("/")
async def related_films(
    sort: str = Query(default="-imdb_rating"),
    page_size: int = Query(default=50, gt=0),
    page_number: int = Query(default=1, gt=0),
    film_service: FilmService = Depends(get_film_service),
):
    """Эндпоинт - /api/v1/films/ - возвращающий список жанров постранично
    - /films/?sort=-imdb_rating&page_size=50&page_number=1 - для запроса по кол-ву жанров и странице"""
    films_list = await film_service.get_info_films()
    if sort[0] == "-":
        value = sort[1:]
        reverse = True
    else:
        value = sort
        reverse = False
    films = sorted(
        films_list,
        key=lambda x: x.__dict__[value] if isinstance(x.__dict__[value], float) else 0,
        reverse=reverse,
    )
    first_number = (page_number - 1) * page_size
    if first_number >= len(films) or len(films) == 0:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="page not found")
    second_number = first_number + page_size
    return films[first_number:second_number]


@router.get("/search/")
async def source_films(query, film_service: FilmService = Depends(get_film_service)):
    films_list = await film_service.search_films(query)
    if not films_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return films_list
