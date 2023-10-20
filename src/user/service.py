from typing import Optional
from fastapi import Request

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_

from src.auth.models import User
from src.user.dao import ReviewDAO

from ..auth.dao import UserDAO
from ..auth.service import DatabaseManager as AuthManager
from ..films.service import DatabaseManager as FilmManager
from ..films.models import Film

from . import schemas


class UserFilmCRUD:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_user_list(self, token: str, film_id: int, list_type: str):

        LIST_TYPES = {
            "favorite": "favorite_films",
            "postponed": "postponed_films",
            "abondoned": "abondoned_films",
            "finished": "finished_films",
            "current": "current_films",
        }

        auth_manager = AuthManager(self.db)
        film_manager = FilmManager(self.db)
        user_crud = auth_manager.user_crud
        film_crud = film_manager.film_crud
                
        user = await user_crud.get_user_by_access_token(access_token=token)
        film = await film_crud.get_film(film_id=film_id)
        
        if not film:
            return {"Message": "Film was not found"}

        if list_type in LIST_TYPES:
            user_list_attribute = LIST_TYPES[list_type]
        else:
            return {"Message": "Invalid list type"}

        user_list = getattr(user, user_list_attribute, [])
        user_update_data = {user_list_attribute: user_list}
            
        if film_id not in user_list:

            user_list.append({"id": film_id, "title": film.title, "poster": film.poster, "rating": film.average_rating})
            user_update = await UserDAO.update(self.db, User.id == user.id, obj_in=user_update_data)
            
            self.db.add(user_update)
            await self.db.commit()
            await self.db.refresh(user_update)
            
            return f"Added to {list_type}"
        
        else:
            user_list.remove({"id": film_id, "title": film.title, "poster": film.poster, "rating": film.average_rating})
            user_update = await UserDAO.update(self.db, User.id == user.id, obj_in=user_update_data)
            
            self.db.add(user_update)
            await self.db.commit()
            await self.db.refresh(user_update)
            
            return f"Deleted from {list_type}"
    

    async def create_review(self, review: schemas.ReviewCreate):

        auth_manager = AuthManager(self.db)
        film_manager = FilmManager(self.db)
        user_crud = auth_manager.user_crud
        film_crud = film_manager.film_crud
                
        film = await film_crud.get_film(film_id=review.film_id)
        if not film: 
            return {"Message": "No film found"}

        db_review = await ReviewDAO.add(
            self.db,
            schemas.ReviewCreate(
                **review.model_dump(),
            )
        )

        self.db.add(db_review)
        await self.db.commit()
        await self.db.refresh(db_review)

        return db_review





class DatabaseManager:
    """
    Класс для управления всеми CRUD-классами и применения изменений к базе данных.

    Args:
        db (AsyncSession): Сессия базы данных SQLAlchemy.

    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_film_crud = UserFilmCRUD(db)

    async def commit(self):
        await self.db.commit()
