from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User

from . import schemas
from . import exceptions

from .dao import ReviewDAO
from .models import Review

from ..utils import check_record_existence
from ..auth.service import DatabaseManager as AuthManager
from ..films.service import DatabaseManager as FilmManager



class ReviewCRUD:

    def __init__(self, db: AsyncSession):
        self.db = db  

    async def create_review(self, token: str, review: schemas.ReviewCreate):

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
    

    async def get_all_reviews(self, *filter, offset: int = 0, limit: int = 100, **filter_by) -> list[Review]:

        reviews = await ReviewDAO.find_all(self.db, *filter, offset=offset, limit=limit, **filter_by)

        return reviews

    async def update_review(self, review_id: int, review_in: schemas.ReviewUpdate):
        
        review_update = await ReviewDAO.update(
            self.db,
            Review.id == review_id,
            obj_in=review_in)

        await self.db.commit()

        return review_update

    async def delete_review(self, review_title: str = None, review_id: int = None) -> None:

        await ReviewDAO.delete(self.db, or_(
            review_id == Review.id,
            review_title == Review.title))

        await self.db.commit()
    

    async def rate_the_review(self, user_id: str, review_id: int, action: str):

        review = await check_record_existence(self.db, Review, review_id)

        obj_in = await self._toggle_review_reaction(review, user_id, action)
        review_update = await ReviewDAO.update(self.db, Review.id == review_id, obj_in=obj_in)

        self.db.add(review_update)
        await self.db.commit()
        await self.db.refresh(review_update)

        return await self._get_review_rating(review)


    async def _toggle_review_reaction(self, review: Review, user_id: str, action: str):
        liked_by_users = set(review.liked_by_users)
        disliked_by_users = set(review.disliked_by_users)

        if action == 'like':
            if user_id in liked_by_users:
                liked_by_users.remove(user_id)
            else:
                liked_by_users.add(user_id)
                disliked_by_users.discard(user_id)
        elif action == 'dislike':
            if user_id in disliked_by_users:
                disliked_by_users.remove(user_id)
            else:
                disliked_by_users.add(user_id)
                liked_by_users.discard(user_id)

        return {
            "liked_by_users": list(liked_by_users),
            "disliked_by_users": list(disliked_by_users)
        }
        
    async def _get_review_rating(self, review: Review):

        return len(review.liked_by_users) - len(review.disliked_by_users)
        
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
