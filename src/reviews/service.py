from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

from loguru import logger

from . import schemas
from . import exceptions

from .dao import ReviewDAO
from .models import Review

from ..auth.service import DatabaseManager as AuthManager
from ..films.service import DatabaseManager as FilmManager



class ReviewCRUD:

    def __init__(self, db: AsyncSession):
        self.db = db  

    async def create_review(self, token: str, review: schemas.ReviewCreate):
        logger.debug(f"создаю ревью {review}")
        auth_manager = AuthManager(self.db)
        film_manager = FilmManager(self.db)
        user_crud = auth_manager.user_crud
        film_crud = film_manager.film_crud
        
        user = await user_crud.get_user_by_access_token(access_token=token)
                
        film = await film_crud.get_film(film_id=review.film_id)
        if not film: 
            raise exceptions.FilmWasNotFound

        db_review = await ReviewDAO.add(
            self.db,
            schemas.ReviewCreateDB(
                **review.model_dump(),
                user_id=user.id,
                username=user.username,
            )
        )

        self.db.add(db_review)
        await self.db.commit()
        await self.db.refresh(db_review)

        return db_review

    async def get_review(self, review_id: int) -> Review:
        logger.debug(f"Получаю  ревью {review_id}")
        review = await ReviewDAO.find_one_or_none(self.db, Review.id == review_id)
        
        return review
    

    async def get_all_reviews(self, *filter, offset: int = 0, limit: int = 100, **filter_by) -> list[Review]:
        logger.info("Получаю все ревьюшки")
        reviews = await ReviewDAO.find_all(self.db, *filter, offset=offset, limit=limit, **filter_by)
        logger.debug(f"Ревьюшки: {reviews}")
        return reviews

    async def update_review(self, review_id: int, review_in: schemas.ReviewUpdate):
        logger.debug(f"Обновляю ревьюшку {review_id} на {review_in}")
        review_update = await ReviewDAO.update(
            self.db,
            Review.id == review_id,
            obj_in=review_in)

        await self.db.commit()

        return review_update

    async def delete_review(self, review_title: str = None, review_id: int = None) -> None:
        logger.debug(f"Удаляю {review_title} c id: {review_id}")
        await ReviewDAO.delete(self.db, or_(
            review_id == Review.id,
            review_title == Review.title))

        await self.db.commit()
    
        
class DatabaseManager:
    """
    Класс для управления всеми CRUD-классами и применения изменений к базе данных.

    Args:
        db (AsyncSession): Сессия базы данных SQLAlchemy.

    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.review_crud = ReviewCRUD(db)

    async def commit(self):
        await self.db.commit()
