from typing import Optional
from fastapi import Request

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_

from src.auth.models import User

from ..auth.dao import UserDAO
from ..auth.service import DatabaseManager as AuthManager
from ..films.models import Film

from . import schemas


class UserFilmCRUD:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_user_list(self, token: str, film_id: str, list_type: str):

        auth_manager = AuthManager(self.db)
        token_crud = auth_manager.token_crud
        user_crud = auth_manager.user_crud

        token = token.split()[1]
        user_id = await token_crud.get_access_token_payload(access_token=token)

        user = await user_crud.get_existing_user(user_id=user_id)

        match list_type:
            case "favorite":
                user_list = user.favorite_films or []
                user_update_data = {"favorite_films": user_list}
            case "postponed":
                user_list = user.postponed_films or []
                user_update_data = {"postponed_films": user_list}
            case "abondoned":
                user_list = user.abondoned_films or []
                user_update_data = {"abondoned_films": user_list}
            case "finished":
                user_list = user.finished_films or []
                user_update_data = {"finished_films": user_list}
            case "current":
                user_list = user.current_films or []
                user_update_data = {"current_films": user_list}
            case _:
                return {"Message": "Invalid list type"}

        if film_id not in user_list:
            user_list.append(film_id)

            user_update = await UserDAO.update(self.db, User.id == user_id, obj_in=user_update_data)
            self.db.add(user_update)

            await self.db.commit()
            await self.db.refresh(user_update)
            return f"Added to {list_type}"

        else:
            user_list.remove(film_id)
            user_update = await UserDAO.update(self.db, User.id == user_id, obj_in=user_update_data)
            self.db.add(user_update)

            await self.db.commit()
            await self.db.refresh(user_update)
            return f"Deleted from {list_type}"


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
