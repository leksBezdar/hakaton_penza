from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas

from .service import DatabaseManager

from ..database import get_async_session


router = APIRouter()


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
      token=token,film_id=film_id, list_type=list_type)


@router.post("/rate_the_film")
async def rate_the_film(
    rating_data: schemas.UserFilmRatingCreate,
    db: AsyncSession = Depends(get_async_session)
):

    db_manager = DatabaseManager(db)
    user_film_crud = db_manager.user_film_crud 
    
    return await user_film_crud.rate_the_film(rating_data)


@router.patch('/rate_review')
async def rate_review(
    user_id: str,
    review_id: int,
    action: str,
    db: AsyncSession = Depends(get_async_session)):

    db_manager = DatabaseManager(db)
    user_review_crud = db_manager.user_review_crud

    return await user_review_crud.rate_the_review(user_id, review_id, action)


@router.get("/get_ratings_for_film")
async def get_ratings_for_film(
    film_id: int,
    db: AsyncSession = Depends(get_async_session)
):

    db_manager = DatabaseManager(db)
    user_film_crud = db_manager.user_film_crud
    
    return await user_film_crud.get_ratings_for_film(film_id)