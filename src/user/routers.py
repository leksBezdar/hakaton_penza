from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Optional

from src.user.models import Review

from . import schemas

from ..films.models import Film
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
      token=token, film_id=film_id, list_type=list_type)


# Регистрация нового пользователя
@router.post("/create_review/", response_model=schemas.ReviewBase)
async def create_review(
    review_data: schemas.ReviewCreate,
    db: AsyncSession = Depends(get_async_session),
) -> Review:

    db_manager = DatabaseManager(db)
    user_film_crud = db_manager.user_film_crud

    return await user_film_crud.create_review(review=review_data)