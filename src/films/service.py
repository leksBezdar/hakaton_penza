from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_

from ..auth.models import User
from ..auth.dao import UserDAO
from ..auth.service import DatabaseManager as AuthManager, TokenCrud

from ..utils import check_record_existence

from .dao import FilmDAO
from .models import Film

from . import schemas
from . import exceptions


class FilmCRUD:
    """
    Класс для выполнения круд-операций с моделью Film.

    Args:
        db (AsyncSession): Сессия базы данных SQLAlchemy.

    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_film(self, film: schemas.FilmCreate) -> Film:
        """
        Создает новую запись о фильме в базе данных.

        Args:
            film (schemas.FilmCreate): Данные о фильме для создания.

        Returns:
            Film: Созданная запись о фильме.

        """

        db_film = await FilmDAO.add(
            self.db,
            schemas.FilmCreate(
                **film.model_dump(),
            )
        )

        self.db.add(db_film)
        await self.db.commit()
        await self.db.refresh(db_film)

        return db_film

    async def get_film(self, film_id: int = None, token: str = None) -> Optional[Film]:
        """
        Получает информацию о фильме по его названию или идентификатору.

        Args:
            film_title (str, optional): Название фильма для поиска.
            film_id (int, optional): Идентификатор фильма для поиска.

        Returns:
            Optional[Film]: Запись о фильме, если найдена, в противном случае None.

        """
        film = await FilmDAO.find_one_or_none(self.db, Film.id == film_id)

        return film

    async def get_all_films(self, *filter, offset: int = 0, limit: int = 100, **filter_by) -> list[Film]:
        """
        Получает список фильмов с возможностью фильтрации и пагинации.

        Args:
            filter: Фильтры для запроса (например, Film.year > 2000).
            offset (int, optional): Смещение для пагинации.
            limit (int, optional): Максимальное количество записей для выборки.
            filter_by: Дополнительные фильтры по полям фильма.

        Returns:
            list[Film]: Список фильмов, соответствующих критериям.

        """
        films = await FilmDAO.find_all(self.db, *filter, offset=offset, limit=limit, **filter_by)

        return films

    async def update_film(self, film_id: int, film_in: schemas.FilmUpdate):
        """
        Обновляет информацию о фильме.

        Args:
            film_id (int): Идентификатор фильма для обновления.
            film_in (schemas.FilmUpdate): Данные для обновления.

        Returns:
            Film: Обновленная запись о фильме.

        """

        film_update = await FilmDAO.update(
            self.db,
            Film.id == film_id,
            obj_in=film_in)

        await self.db.commit()

        return film_update

    async def delete_film(self, film_title: str = None, film_id: int = None) -> None:
        """
        Удаляет запись о фильме по названию или идентификатору.

        Args:
            film_title (str, optional): Название фильма для удаления.
            film_id (int, optional): Идентификатор фильма для удаления.

        """
        await FilmDAO.delete(self.db, or_(
            film_id == Film.id,
            film_title == Film.title))

        await self.db.commit()
        

class UserFilmCRUD:
       
    LIST_TYPES = {
            "favorite": "favorite_films",
            "postponed": "postponed_films",
            "abandoned": "abandoned_films",
            "planned": "planned_films",
            "finished": "finished_films",
        }
    

    def __init__(self, db: AsyncSession):
        self.db = db 


    async def update_user_list(self, user_id: str, film_id: int, list_type: str):
        
        film = await check_record_existence(db=self.db, model=Film, record_id=film_id)
        user = await check_record_existence(self.db, User, user_id)
        
        user_list_attribute = self.LIST_TYPES.get(list_type)
        
        if not user_list_attribute:
            raise exceptions.InvalidListType
        
        return await self._update_user_list(user, user_list_attribute, film)

    
    def _create_film_data(self, film: Film) -> dict:
        return {
            "id": film.id, "title": film.title, "poster": film.poster,
            "rating": film.average_rating, "genres": film.genres
        }

    async def _update_user_list(self, user: User, user_list_attribute: str, film: Film):
        
        film_data = self._create_film_data(film=film)
        
        # Получаем текущий список пользователя, который пользователь хочет обновить
        target_user_list = getattr(user, user_list_attribute, [])
        
        if user_list_attribute != "favorite_films":
            
            await self._check_other_user_lists(
                film_data=film_data,
                user=user,
                user_list_attribute=user_list_attribute
            )
        
        await self._toggle_film_data_in_user_list(target_user_list=target_user_list, film=film)

        user_update_data = {user_list_attribute: target_user_list}
        user_update = await UserDAO.update(self.db, User.id == user.id, obj_in=user_update_data)
        
        self.db.add(user_update)
        await self.db.commit()
        await self.db.refresh(user_update)   

        return {"Message": "Update was successful"}
    
    async def _toggle_film_data_in_user_list(self, target_user_list: list, film: Film):
        
        film_data = self._create_film_data(film=film)
            
        if film_data in target_user_list:
            target_user_list.remove(film_data)
            return "Deleted from target_list"
        else:
            target_user_list.append(film_data)
            return f"Added to target_list"
    
    
    async def _check_other_user_lists(self, film_data: dict, user: User, user_list_attribute: str):     
                
        # Проверка, что film_id не находится в других списках и не является записью в списке favorite_films
        other_list_attributes = [key for key in self.LIST_TYPES.values()if key != user_list_attribute and key != "favorite_films"]
 
        for other_list_attribute in other_list_attributes:
            
            other_list = getattr(user, other_list_attribute, [])
            
            if film_data in other_list:
                
                # Если film_id найден в другом списке, удаляем его оттуда
                other_list.remove(film_data)
                
                user_update_data = {other_list_attribute: other_list}
                user_update = await UserDAO.update(self.db, User.id == user.id, obj_in=user_update_data)

                self.db.add(user_update)
                await self.db.commit()
                await self.db.refresh(user_update)
                
                return f"deleted from {other_list_attribute}"
     

class DatabaseManager:
    """
    Класс для управления всеми CRUD-классами и применения изменений к базе данных.

    Args:
        db (AsyncSession): Сессия базы данных SQLAlchemy.

    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.film_crud = FilmCRUD(db)
        self.user_film_crud = UserFilmCRUD(db)

    async def commit(self):
        await self.db.commit()
