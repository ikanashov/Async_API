from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from api.v1.models import FilmGenre, FilmGenreDetail, FilmGenreSort, Page

from services.film import FilmService, get_film_service


# Объект router, в котором регистрируем обработчики
router = APIRouter()


@router.get('', response_model=List[FilmGenre])
async def get_all_genre(
    sort: FilmGenreSort = Depends(),
    page: Page = Depends(),
    film_service: FilmService = Depends(get_film_service)
) -> List[FilmGenre]:
    genres = await film_service.get_all_genre(sort.sort, page.page_size, page.page_number)
    return genres


# Для примера берем 5bd77168-c5b1-4c9d-bd1f-1193582d9e66
@router.get('/{genre_id}', response_model=FilmGenreDetail)
async def genre_details(genre_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmGenreDetail:
    genre = await film_service.get_genre_by_id(genre_id)
    if not genre:
        # Если жанр не найден, отдаём 404 статус
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    return genre
