from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas

from .models import Comment
from .service import DatabaseManager

from ..database import get_async_session


router = APIRouter()


@router.post("/create_comment/", response_model=schemas.CommentBase)
async def create_comment(
    film_id: int,
    token: str,
    comment_data: schemas.CommentCreate,
    db: AsyncSession = Depends(get_async_session),
) -> Comment:

    db_manager = DatabaseManager(db)
    comment_crud = db_manager.comment_crud

    return await comment_crud.create_comment(film_id=film_id, token=token, comment=comment_data)


@router.get("/get_all_comments")
async def get_all_comments(
    film_id: int,
    offset: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_async_session),
):
    db_manager = DatabaseManager(db)
    comment_crud = db_manager.comment_crud

    return await comment_crud.get_all_comments(film_id=film_id, offset=offset, limit=limit)


@router.patch("/update_comment", response_model=schemas.CommentUpdate)
async def update_comment(
    comment_id: int,
    comment_data: schemas.CommentUpdate,
    db: AsyncSession = Depends(get_async_session),
):

    db_manager = DatabaseManager(db)
    comment_crud = db_manager.comment_crud

    return await comment_crud.update_comment(comment_id=comment_id, comment_in=comment_data)


@router.delete("/delete_comment")
async def delete_comment(
        comment_id: int = None,
        db: AsyncSession = Depends(get_async_session)):

    db_manager = DatabaseManager(db)
    comment_crud = db_manager.comment_crud

    await comment_crud.delete_comment(comment_id=comment_id)

    response = JSONResponse(content={
        "message": "Delete successful",
    })

    return response