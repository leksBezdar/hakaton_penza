from sqlalchemy.ext.asyncio import AsyncSession

from loguru import logger

from .dao import CommentDAO
from .models import Comment

from ..utils import check_record_existence
from ..auth.service import DatabaseManager as AuthManager
from ..films.models import Film
from ..reviews.models import Review

from . import schemas


class CommentCRUD:
    
    def __init__(self, db: AsyncSession):
        self.db = db 
        
    async def create_comment(self, token: str, comment: schemas.CommentCreate):
        logger.debug(f"Создаю комментарий: {comment}")
        auth_manager = AuthManager(self.db)
        user_crud = auth_manager.user_crud
        
        if comment.film_id:
            await check_record_existence(self.db, Film, comment.film_id)
        if comment.parent_review_id:
            await check_record_existence(self.db, Review, comment.parent_review_id)
        
        user = await user_crud.get_user_by_access_token(access_token=token)

        db_comment = await CommentDAO.add(
            self.db,
            schemas.CommentCreateDB(
                **comment.model_dump(),
                user_id=user.id,
                username=user.username,
            )
        )

        self.db.add(db_comment)
        await self.db.commit()
        await self.db.refresh(db_comment)

        return db_comment
    

    async def get_all_comments(self, *filter, offset: int = 0, limit: int = 100, **filter_by) -> list[Comment]:
        logger.info("Получаю список всех фильмов")
        comments = await CommentDAO.find_all(self.db, *filter, offset=offset, limit=limit, **filter_by)
        logger.debug(f"Список всех фильмов: {comments}")
        return comments

    async def update_comment(self, comment_id: int, comment_in: schemas.CommentUpdate):
        logger.debug(f"Обновляю comment_id: {comment_id} на {comment_in} ")
        comment_update = await CommentDAO.update(
            self.db,
            Comment.id == comment_id,
            obj_in=comment_in)

        await self.db.commit()

        return comment_update

    async def delete_comment(self, comment_id: int = None) -> None:

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
