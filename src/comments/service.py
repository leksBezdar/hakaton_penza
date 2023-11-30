from datetime import datetime
from json import JSONEncoder
import json
from uuid import uuid4
from fastapi import WebSocket

from sqlalchemy.ext.asyncio import AsyncSession

from loguru import logger

from . import schemas
from .dao import CommentDAO, ReplyCommentDAO
from .models import Comment, ReplyComment

from ..utils import check_record_existence, get_unique_id
from ..auth.service import DatabaseManager as AuthManager
from ..films.models import Film
from ..reviews.models import Review



class CommentCRUD:
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.websockets: list[WebSocket] = []
        
    async def create_comment(self, comment: schemas.CommentCreate) -> Comment:
        
        logger.debug(f"Создаю комментарий: {comment}")
        
        comment_id = await get_unique_id()
        
        # Создаем профильные данные гостя
        user_id, username = "0", "Гость"

        if comment.token:
            
            auth_manager = AuthManager(self.db)
            user_crud = auth_manager.user_crud
            
            user = await user_crud.get_user_by_access_token(access_token=comment.token)
            user_id, username = user.id, user.username
            
        if comment.film_id:
            await check_record_existence(self.db, Film, comment.film_id)

        db_comment = await CommentDAO.add(
            self.db,
            schemas.CommentCreateDB(
                **comment.model_dump(),
                id=comment_id,
                user_id=user_id,
                username=username
            ),
        )

        self.db.add(db_comment)
        await self.db.commit()
        await self.db.refresh(db_comment)

        db_reply = await self._check_if_is_reply(comment.parent_comment_id, comment.parent_review_id, comment_id)
        
        response_data = await self._set_responce_comment_data(db_comment, db_reply)

        return response_data 
    
    async def _set_responce_comment_data(self, db_comment: Comment, db_reply: ReplyComment):
        
        response_data = {}
        
        if db_comment is not None:
             response_data.update({
                 "id": db_comment.id,
                 "user_id": db_comment.user_id,
                 "username": db_comment.username,
                 "message": db_comment.message, 
                 "film_id": db_comment.film_id,
                 "created_at": db_comment.created_at
             })
             
        if db_reply is not None:
             response_data.update({
                 "reply_id": db_reply.id,
                 "comment_id": db_reply.comment_id,
                 "parent_comment_id": db_reply.parent_comment_id,
                 "parent_review_id": db_reply.parent_review_id, 
             })
             
        comment_obj_json = json.dumps(response_data, cls=CustomEncoder)
        return comment_obj_json

    async def _create_reply_comment(self, reply_data: schemas.ReplyCommentData):
        
        if reply_data.parent_review_id:
            await check_record_existence(self.db, Review, reply_data.parent_review_id)

        db_reply = await ReplyCommentDAO.add(
            self.db,
            schemas.ReplyCommentCreateDB(
            **reply_data.model_dump(),
            id = await get_unique_id()
            )
        )
        
        self.db.add(db_reply)
        await self.db.commit()
        await self.db.refresh(db_reply)

        return db_reply
    
    async def _check_if_is_reply(self, parent_comment_id: str, parent_review_id: int, comment_id: str):
                
        if parent_comment_id or parent_review_id: 
            reply_data = schemas.ReplyCommentData(
                comment_id=comment_id,
                parent_comment_id=parent_comment_id,
                parent_review_id=parent_review_id
            )
            return await self._create_reply_comment(reply_data)
    
    async def get_all_replies(self, *filter, offset: int = 0, limit: int = 100, **filter_by):

        replies = await ReplyCommentDAO.find_all(self.db, *filter, offset=offset, limit=limit, **filter_by)
        
        return replies


    async def get_all_comments(self, *filter, offset: int = 0, limit: int = 100, **filter_by) -> list[Comment]:
        
        logger.info("Получаю список все коментарии фильма")
        comments = await CommentDAO.find_all(self.db, *filter, offset=offset, limit=limit, **filter_by)
        logger.debug(f"Все комменты фильма: {comments}")
        
        return comments

    async def update_comment(self, comment_id: str, comment_in: schemas.CommentUpdate):
        
        logger.debug(f"Обновляю comment_id: {comment_id} на {comment_in} ")
        comment_update = await CommentDAO.update(
            self.db,
            Comment.id == comment_id,
            obj_in=comment_in)

        await self.db.commit()

        return comment_update

    async def delete_comment(self, comment_id: str = None) -> None:

        await CommentDAO.delete(self.db, comment_id == Comment.id,)

        await self.db.commit()
        
    async def connect(self, webSocket: WebSocket):
        await webSocket.accept()
        self.websockets.append(webSocket)
        
    async def disconnect(self, webSocket: WebSocket):
        self.websockets.remove(webSocket)
    
        
    async def broadcast_comment(self, comment_obj):
        for websocket in self.websockets:
            try:
                await websocket.send_json(comment_obj)
            except Exception as e:
                print(f"Failed to send message to a client: {e}")
                
    async def comment_to_dict(self, comment: Comment): 
            return {
                "id": comment.id,
                "film_id": comment.film_id,
                "user_id": comment.user_id,
                "username": comment.username,
                "message": comment.message,
                "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        
    async def comments_to_dicts(self, comments):
        return [await self.comment_to_dict(comment) for comment in comments]

    @staticmethod
    async def dicts_to_json(data):
        return json.dumps(data, default=str)


class CustomEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)
        

class DatabaseManager:
    """
    Класс для управления всеми CRUD-классами и применения изменений к базе данных.

    Args:
        db (AsyncSession): Сессия базы данных SQLAlchemy.

    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.comment_crud = CommentCRUD(db)

    async def commit(self):
        await self.db.commit()
