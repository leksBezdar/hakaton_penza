from typing import Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from .models import Review
from ..films.models import Film

from ..database import get_async_session

from . import schemas
from .service import DatabaseManager


router = APIRouter()


@router.post("/create_review/", response_model=schemas.ReviewBase)
async def create_review(
    token: str,
    review_data: schemas.ReviewCreate,
    db: AsyncSession = Depends(get_async_session),
) -> Review:

    db_manager = DatabaseManager(db)
    review_crud = db_manager.review_crud

    return await review_crud.create_review(token=token, review=review_data)


@router.get("/get_all_reviews")
async def get_all_reviews(
    film_id: int = None,
    offset: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_async_session),
):
    db_manager = DatabaseManager(db)
    review_crud = db_manager.review_crud

    return await review_crud.get_all_reviews(film_id=film_id, offset=offset, limit=limit)


@router.patch("/update_review", response_model=schemas.ReviewUpdate)
async def update_review(
    review_id: int,
    review_data: schemas.ReviewUpdate,
    db: AsyncSession = Depends(get_async_session),
):

    db_manager = DatabaseManager(db)
    review_crud = db_manager.review_crud

    return await review_crud.update_review(review_id=review_id, review_in=review_data)


@router.delete("/delete_review")
async def delete_review(
        review_title: str = None,
        review_id: int = None,
        db: AsyncSession = Depends(get_async_session)):

    db_manager = DatabaseManager(db)
    review_crud = db_manager.review_crud

    await review_crud.delete_review(review_title=review_title, review_id=review_id)

    response = JSONResponse(content={
        "message": "Delete successful",
    })

    return response