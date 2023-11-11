from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from loguru import logger

from . import schemas
from .dao import CommentDAO, ReplyCommentDAO
from .models import Comment

from ..utils import check_record_existence
from ..auth.service import DatabaseManager as AuthManager
from ..films.models import Film
from ..reviews.models import Review



class CommentCRUD:
    
    def __init__(self, db: AsyncSession):
        self.db = db 
        
    async def create_comment(self, token: str, comment: schemas.CommentCreate, parent_comment_id: str, parent_review_id: int):    
        
        comment_id = str(uuid4())
                
        if comment.film_id:
            await check_record_existence(self.db, Film, comment.film_id)     
        
        logger.debug(f"Создаю комментарий: {comment}")
        
        auth_manager = AuthManager(self.db)
        user_crud = auth_manager.user_crud       
        user = await user_crud.get_user_by_access_token(access_token=token)
        
        db_comment = await CommentDAO.add(
            self.db,
            schemas.CommentCreateDB(
                **comment.model_dump(),
                id=comment_id,
                user_id=user.id,
                username=user.username,
            )
        )
        
        self.db.add(db_comment)
        await self.db.commit()
        await self.db.refresh(db_comment)

        await self._check_if_is_reply(parent_comment_id, parent_review_id, comment_id)
        
        return db_comment
    
    async def _create_reply_comment(self, reply_data: schemas.ReplyCommentData):
        
        if reply_data.parent_review_id:
            await check_record_existence(self.db, Review, reply_data.parent_review_id)

        db_reply = await ReplyCommentDAO.add(
            self.db,
            schemas.ReplyCommentCreateDB(
            **reply_data.model_dump(),
            id = str(uuid4())
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
            await self._create_reply_comment(reply_data)
    
    async def get_all_replies(self, *filter, offset: int = 0, limit: int = 100, **filter_by):

        replies = await ReplyCommentDAO.find_all(self.db, *filter, offset=offset, limit=limit, **filter_by)
        
        return replies


    async def get_all_comments(self, *filter, offset: int = 0, limit: int = 100, **filter_by) -> list[Comment]:
        
        logger.info("Получаю список все коментаррии фильма")
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
