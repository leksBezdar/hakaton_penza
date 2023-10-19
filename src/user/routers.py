from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Optional

from . import schemas

from ..films.models import Film
from .service import DatabaseManager
from ..database import get_async_session


router = APIRouter()


@router.post("/update_user_list")
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