from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas

from .models import Film
from .service import DatabaseManager

from ..database import get_async_session


router = APIRouter()


@router.post("/create_film/", response_model=schemas.FilmCreate)
async def create_film(
        film_data: schemas.FilmCreate,
        db: AsyncSession = Depends(get_async_session)) -> Film:
    db_manager = DatabaseManager(db)
    film_crud = db_manager.film_crud

    return await film_crud.create_film(film=film_data)


@router.get("/get_film/", response_model=schemas.FilmRead)
async def get_film(
    token: str = None,
    film_id: int = None,
    db: AsyncSession = Depends(get_async_session),
) -> Film:
    db_manager = DatabaseManager(db)
    film_crud = db_manager.film_crud

    return await film_crud.get_film(token=token, film_id=film_id)


@router.get("/get_all_films")
async def get_all_films(
    offset: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_async_session),
):
    db_manager = DatabaseManager(db)
    film_crud = db_manager.film_crud

    return await film_crud.get_all_films(offset=offset, limit=limit)


@router.patch("/update_film", response_model=schemas.FilmUpdate)
async def update_film(
    film_id: int,
    film_data: schemas.FilmUpdate,
    db: AsyncSession = Depends(get_async_session),
):

    db_manager = DatabaseManager(db)
    film_crud = db_manager.film_crud

    return await film_crud.update_film(film_id=film_id, film_in=film_data)



@router.patch("/update_user_list")
async def update_user_list(
    token: str,
    film_id: int,
    list_type: str,
    db: AsyncSession = Depends(get_async_session),
):
      
    db_manager = DatabaseManager(db)
    user_film_crud = db_manager.user_film_crud
    
    return await user_film_crud.update_user_list(
      token=token, film_id=film_id, list_type=list_type)


@router.delete("/delete_film")
async def delete_film(
        film_title: str = None,
        film_id: int = None,
        db: AsyncSession = Depends(get_async_session)):

    db_manager = DatabaseManager(db)
    film_crud = db_manager.film_crud

    await film_crud.delete_film(film_title=film_title, film_id=film_id)

    response = JSONResponse(content={
        "message": "Delete successful",
    })

    return response
