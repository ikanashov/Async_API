from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from models.api.v1 import FilmGenre, FilmGenreDetail, FilmGenreSort, Page

from services.film import FilmService, get_film_service


router = APIRouter()


@router.get(
    '',
    response_model=List[FilmGenre],
    summary='Список жанров',
    description='Список жанров с пагинацией',
    response_description='uuid, название'
)
async def get_all_genre(
    sort: FilmGenreSort = Depends(),
    page: Page = Depends(),
    film_service: FilmService = Depends(get_film_service)
) -> List[FilmGenre]:
    genres = await film_service.get_all_genre(sort.sort, page.page_size, page.page_number)
    return genres


@router.get(
    '/{genre_id}',
    response_model=FilmGenreDetail,
    summary='Подробная информация о жанре',
    description='Вывод подробной информации о жанре',
    response_description='uuid, название, описание'
)
async def genre_details(genre_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmGenreDetail:
    genre = await film_service.get_genre_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return genre
