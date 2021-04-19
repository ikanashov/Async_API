from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from api.v1.models import FilmDetail, FilmGenreFilter, FilmQuery, FilmShort, FilmSort, Page

from services.film import FilmService, get_film_service


# Объект router, в котором регистрируем обработчики
router = APIRouter()


@router.get('', response_model=List[FilmShort], tags=['genre'])
async def get_all_film(
    genre_filter: FilmGenreFilter = Depends(),
    sort: FilmSort = Depends(),
    page: Page = Depends(),
    film_service: FilmService = Depends(get_film_service)
) -> List[FilmShort]:
    films = await film_service.get_all_film(sort.sort, page.page_size, page.page_number, genre_filter.genre_filter)
    return films


@router.get('/search', response_model=List[FilmShort])
async def search_film(
    query: FilmQuery = Depends(),
    page: Page = Depends(),
    film_service: FilmService = Depends(get_film_service)
) -> List[FilmShort]:
    films = await film_service.search_film(query.query, page.page_size, page.page_number)
    return films


# Внедряем FilmService с помощью Depends(get_film_service)
@router.get('/{film_id}', response_model=FilmDetail)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmDetail:
    film = await film_service.get_film_by_id(film_id)
    if not film:
        # Если фильм не найден, отдаём 404 статус
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return film
