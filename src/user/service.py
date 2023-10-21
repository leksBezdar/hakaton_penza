from typing import Optional
from fastapi import Request

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_

from src.auth.models import User
from src.user.dao import ReviewDAO
from src.user.models import Review

from ..utils import check_record_existence
from ..auth.dao import UserDAO
from ..auth.service import DatabaseManager as AuthManager
from ..films.service import DatabaseManager as FilmManager
from ..films.models import Film

from . import schemas


class UserFilmCRUD:
       
    LIST_TYPES = {
            "favorite": "favorite_films",
            "postponed": "postponed_films",
            "abandoned": "abandoned_films",
            "finished": "finished_films",
            "current": "current_films",
        }
    

    def __init__(self, db: AsyncSession):
        self.db = db


    async def update_user_list(self, token: str, film_id: int, list_type: str):

        user, user_list_attribute = await self._get_user_and_list_attribute(token, list_type)
        film = await check_record_existence(db=self.db, model=Film, record_id=film_id)

        if not user_list_attribute:
            return {"Message": "Invalid list type"}
        
        action_message = await self._update_user_list(user, user_list_attribute, film)

        return action_message
    

    async def _get_user_and_list_attribute(self, token, list_type):
        
        auth_manager = AuthManager(self.db)
        user_crud = auth_manager.user_crud
        
        user = await user_crud.get_user_by_access_token(access_token=token)
        user_list_attribute = self.LIST_TYPES.get(list_type)
        
        return user, user_list_attribute
    

    async def _update_user_list(self, user, user_list_attribute, film):
        
        user_list = getattr(user, user_list_attribute, [])
        film_data = {"id": film.id, "title": film.title, "poster": film.poster, "rating": film.average_rating}

        if film_data in user_list:
            # Удаление фильма из списка
            user_list.remove(film_data)
            action_message = f"Deleted from {user_list_attribute}"
        else:
            # Добавление фильма в список
            user_list.append(film_data)
            action_message = f"Added to {user_list_attribute}"

        user_update_data = {user_list_attribute: user_list}
        user_update = await UserDAO.update(self.db, User.id == user.id, obj_in=user_update_data)
        
        self.db.add(user_update)
        await self.db.commit()
        await self.db.refresh(user_update)

        return action_message

        

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
            return {"Message": "No film found"}

        db_review = await ReviewDAO.add(
            self.db,
            schemas.ReviewCreateDB(
                user_id=user.id,
                **review.model_dump(),
            )
        )

        self.db.add(db_review)
        await self.db.commit()
        await self.db.refresh(db_review)

        return db_review
    

    async def get_all_reviews(self, *filter, offset: int = 0, limit: int = 100, **filter_by) -> list[Review]:

        films = await ReviewDAO.find_all(self.db, *filter, offset=offset, limit=limit, **filter_by)

        return films

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





class DatabaseManager:
    """
    Класс для управления всеми CRUD-классами и применения изменений к базе данных.

    Args:
        db (AsyncSession): Сессия базы данных SQLAlchemy.

    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_film_crud = UserFilmCRUD(db)
        self.review_crud = ReviewCRUD(db)

    async def commit(self):
        await self.db.commit()
