from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas

from .models import Comment
from .service import DatabaseManager, ConnectionManager

from ..database import get_async_session


router = APIRouter()
connection_manager = ConnectionManager()


@router.websocket("/ws/comment/create/{film_id}")
async def create_comment_ws(
    film_id: int,
    websocket: WebSocket,
    db: AsyncSession = Depends(get_async_session),
):
    db_manager = DatabaseManager(db)
    comment_crud = db_manager.comment_crud

    await connection_manager.connect(film_id, websocket)

    try:
        while True:
            comment_data = await websocket.receive_json()
            comment = schemas.CommentCreate(**comment_data)

            comment_obj = await comment_crud.create_comment(
                comment=comment,
            )
            await connection_manager.broadcast(film_id, comment_obj)

    except WebSocketDisconnect:
        await connection_manager.disconnect(film_id, websocket)


@router.post("/create_comment/", response_model=schemas.CommentBase)
async def create_comment(
    comment_data: schemas.CommentCreate,
    db: AsyncSession = Depends(get_async_session),
) -> Comment:

    db_manager = DatabaseManager(db)
    comment_crud = db_manager.comment_crud

    comment_obj = await comment_crud.create_comment(comment=comment_data)

    return comment_obj


@router.get("/get_all_comments")
async def get_all_comments(
    film_id: int = None,
    offset: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_async_session),
):
    db_manager = DatabaseManager(db)
    comment_crud = db_manager.comment_crud

    return await comment_crud.get_all_comments(film_id=film_id, offset=offset, limit=limit)


@router.patch("/update_comment", response_model=schemas.CommentUpdate)
async def update_comment(
    comment_id: str,
    comment_data: schemas.CommentUpdate,
    db: AsyncSession = Depends(get_async_session),
):

    db_manager = DatabaseManager(db)
    comment_crud = db_manager.comment_crud

    return await comment_crud.update_comment(comment_id=comment_id, comment_in=comment_data)


@router.delete("/delete_comment")
async def delete_comment(
    comment_id: str = None,
    db: AsyncSession = Depends(get_async_session)
):

    db_manager = DatabaseManager(db)
    comment_crud = db_manager.comment_crud

    await comment_crud.delete_comment(comment_id=comment_id)

    response = JSONResponse(content={
        "message": "Delete successful",
    })

    return response


@router.get("/get_all_replies")
async def get_all_replies(
    parent_review_id: int = None,
    parent_comment_id: str = None,
    offset: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_async_session)
):

    db_manager = DatabaseManager(db)
    comment_crud = db_manager.comment_crud

    replies = await comment_crud.get_all_replies(
        parent_review_id=parent_review_id,
        parent_comment_id=parent_comment_id,
        offset=offset, limit=limit)

    return replies
