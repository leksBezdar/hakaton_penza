from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_

from .dao import FilmDAO
from .models import Film

from . import schemas


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

    async def get_film(self, film_title: str = None, film_id: int = None) -> Optional[Film]:
        """
        Получает информацию о фильме по его названию или идентификатору.

        Args:
            film_title (str, optional): Название фильма для поиска.
            film_id (int, optional): Идентификатор фильма для поиска.

        Returns:
            Optional[Film]: Запись о фильме, если найдена, в противном случае None.

        """
        film = await FilmDAO.find_one_or_none(self.db, or_(
            Film.title == film_title,
            Film.id == film_id))

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

        obj_in = {}
        for key, value in film_in.model_dump().items():
            if value is not None:
                obj_in[key] = value

        film_update = await FilmDAO.update(
            self.db,
            Film.id == film_id,
            obj_in=obj_in)

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


class DatabaseManager:
    """
    Класс для управления всеми CRUD-классами и применения изменений к базе данных.

    Args:
        db (AsyncSession): Сессия базы данных SQLAlchemy.

    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.film_crud = FilmCRUD(db)

    async def commit(self):
        await self.db.commit()
