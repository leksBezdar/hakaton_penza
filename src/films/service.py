from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, or_, select

from loguru import logger

from ..auth.models import User
from ..auth.dao import UserDAO
from ..auth.service import DatabaseManager as AuthManager

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
        
        if await self._check_existing_film(film.title, film.trailer, film.poster):
            raise exceptions.FilmAlreadyExists

        db_film = await FilmDAO.add(
            self.db,
            schemas.FilmCreate(
                **film.model_dump(),
            )
        )
        
        logger.debug(f"Создаю фильм: {film}")
        self.db.add(db_film)
        await self.db.commit()
        await self.db.refresh(db_film)

        return db_film

    async def get_film(self, film_id: int = None) -> Film | None:
        """
        Получает информацию о фильме по его названию или идентификатору.

        Args:
            film_title (str, optional): Название фильма для поиска.
            film_id (int, optional): Идентификатор фильма для поиска.

        Returns:
            Optional[Film]: Запись о фильме, если найдена, в противном случае None.

        """
        logger.debug(f"Пытаюсь найти фильм с film_id: {film_id}")
        film = await FilmDAO.find_one_or_none(self.db, Film.id == film_id)

        return film

    async def get_all_films(self, *filter, offset: int = 0, limit: int = 100, **filter_by) -> list[Film]:
        logger.info("Получаю все фильмы")
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
        logger.debug(f"Все фильмы: {films}")

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
        logger.debug(f"Обновляю информацию. Film_id: {film_id} на {film_in}")
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
        logger.debug(f"Удаляю фильм film_title: {film_title} | film_id: {film_id}")
        await FilmDAO.delete(self.db, or_(
            film_id == Film.id,
            film_title == Film.title))

        await self.db.commit()
        
        
    async def _check_existing_film(self, title: str, trailer: str, poster: str) -> bool:
        
        film = await FilmDAO.find_one_or_none(self.db, or_(
            Film.title == title,
            Film.poster == poster,
            Film.trailer == trailer
        ))
        
        return bool(film)

        
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
