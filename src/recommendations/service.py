from random import sample
from sqlalchemy import select

from loguru import logger

from sqlalchemy.ext.asyncio import AsyncSession

from .config import SIMILARITY_COEFFICIENT
from .config import THRESHOLD_FOR_POSITIVE_RATING
from .config import NUM_GENRES

from ..films.dao import FilmDAO
from ..films.models import Film
from ..user_actions.models import UserFilmRating

class Recommendations:
    """
    Класс Recommendations предоставляет методы для генерации рекомендаций фильмов для пользователей
    на основе их рейтингов и жанров.

    Args:
        db (AsyncSession): Сессия для работы с базой данных.

    Attributes:
        db (AsyncSession): Сессия для работы с базой данных.
        user_positive_ratings (List[tuple]) | None: Список фильмов, оцененных пользователем положительно.
        user_negative_ratings (List[tuple]) | None: Список фильмов, оцененных пользователем отрицательно.
    """
    
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.user_high_rated_films = None
        self.user_low_rated_films = None

    async def _get_recent_ratings(self, user_id: str, limit: int = 20) -> list[tuple[int, float]]:
        
        """
        Получает недавние рейтинги пользователя.

        Args:
            user_id (str): Идентификатор пользователя.
            limit (int, optional): Максимальное количество рейтингов для получения. По умолчанию 20.

        Returns:
            list[tuple[int, float]]: Список кортежей, где каждый кортеж содержит идентификатор фильма и его рейтинг.
        """

        try:
            query = (
                select(UserFilmRating.film_id, UserFilmRating.rating)
                .where(UserFilmRating.user_id == user_id)
                .order_by(UserFilmRating.id.desc())
                .limit(limit)
            )
                
            result = await self.db.execute(query)            
            user_ratings = result.fetchall()
            
            return user_ratings
        
        except Exception as e:
            logger.opt(exception=e).critical("Error in _get_recent_ratings")
            raise

    async def _get_user_high_rated_films(self, user_ratings: list) -> tuple[int]:
        
        """
        Возвращает список фильмов, оцененных пользователем положительно.

        Args:
            user_ratings (list): Список кортежей (film_id, rating).

        Returns:
            tuple[int]: Кортеж идентификаторов фильмов, оцененных положительно.
        """
        
        if self.user_high_rated_films:
            return self.user_high_rated_films
        
        self.user_high_rated_films = tuple([film_id for film_id, rating in user_ratings if rating >= float(THRESHOLD_FOR_POSITIVE_RATING)])
        return self.user_high_rated_films

    async def _get_user_low_rated_films(self, user_ratings: list) -> tuple[int]:
        
        """
        Возвращает список фильмов, оцененных пользователем отрицательно.

        Args:
            user_ratings (list): Список кортежей (film_id, rating).

        Returns:
            tuple[int]: Кортеж идентификаторов фильмов, оцененных положительно.
        """
        
        if self.user_low_rated_films:
            return self.user_low_rated_films
        
        self.user_low_rated_films = tuple([film_id for film_id, rating in user_ratings if rating < float(THRESHOLD_FOR_POSITIVE_RATING)])
        return self.user_low_rated_films
    
    async def _get_suitable_films(self, user_ratings: list, all_films: tuple[Film]) -> tuple[int]:
        
        """
        Возвращает фильмы, подходящие для рекомендаций пользователю.

        Args:
            user_ratings (list): Список кортежей (film_id, rating).
            all_films (tuple[Film]): Все фильмы в базе данных.

        Returns:
            tuple[int]: Фильмы, подходящие для рекомендаций (исключая уже оцененные).
        """
        
        try:
            
            user_high_rated_films = await self._get_user_high_rated_films(user_ratings)
            user_low_rated_films = await self._get_user_low_rated_films(user_ratings)

            user_rated_films = user_high_rated_films + user_low_rated_films
            
            if not user_rated_films:
                return all_films
            
            suitable_films = tuple([film for film in all_films if film.id not in user_rated_films])
            
            return suitable_films
        
        except Exception as e:
            print(f"Error in _get_suitable_films: {e}")
            raise 

    async def _calculate_genre_coefficients(self, user_positive_films: list, all_films: tuple[Film]) -> dict:
        """
        Рассчитывает коэффициенты заинтересованности в жанрах на основе оцененных пользователем фильмов.

        Args:
            user_positive_films (List[int]): Список идентификаторов фильмов, оцененных положительно.
            all_films (tuple[Film]): Все фильмы в базе данных.

        Returns:
            dict: Словарь, где ключи - жанры, значения - их коэффициенты заинтересованности.
        """
        genre_count = {}
        total_genres = 0

        for film_id in user_positive_films:
            film = next((film for film in all_films if film.id == film_id), None)
            if film:
                total_genres += len(film.genres)
                for genre in film.genres:
                    genre_count[genre] = genre_count.get(genre, 0) + 1

        genre_coefficients = {genre: count / total_genres for genre, count in genre_count.items()}
        
        return genre_coefficients

    async def _get_most_common_genres(self, user_positive_films: list, all_films: tuple[Film]) -> list[str]:
        """
        Возвращает наиболее часто встречающиеся жанры среди фильмов, оцененных положительно пользователем,
        учитывая коэффициенты заинтересованности.

        Args:
            user_positive_films (List[int]): Список идентификаторов фильмов, оцененных положительно.
            all_films (tuple[Film]): Все фильмы в базе данных.

        Returns:
            List[str]: Список наиболее популярных жанров среди положительных оценок.
        """
        genre_coefficients = await self._calculate_genre_coefficients(user_positive_films, all_films)

        sorted_most_commot_genres = dict(sorted(genre_coefficients.items(), key=lambda item: item[1], reverse=True))
        
        target_genres = dict(list(sorted_most_commot_genres.items())[:int(NUM_GENRES)+1])

        return target_genres
    
    async def _get_random_related_films(self, num_additional_films: int, all_films: tuple[Film], user_ratings: list) -> list[int]:
        
        """
        Возвращает случайные фильмы, которые связаны с предпочтениями пользователя.
        Вызывается в случае недостатка наиболее схожих фильмов.

        Args:
            num_additional_films (int): Количество недостающих фильмов для рекомендации.
            all_films (tuple[Film]): Все фильмы в базе данных.
            user_ratings (list): Список кортежей с оценками пользователя(film_id, rating).

        Returns:
            List[int]: Список случайных фильмов.
        """
        
        try:
            suitable_films = await self._get_suitable_films(user_ratings, all_films)
            
            if len(suitable_films) <= num_additional_films:
                random_related_films = suitable_films
            else:
                random_related_films = sample(suitable_films, num_additional_films)

            return random_related_films
        
        except Exception as e:
            logger.opt(exception=e).critical("Error in _get_random_related_films")
            raise
        
    async def _get_recommended_films(self,
        num_films: int,
        all_films: tuple[Film],
        user_ratings: list) -> set[Film]:
        
        """
        Генерирует рекомендации фильмов для пользователя.

        Args:
            num_films (int): Количество фильмов для рекомендации.
            all_films (tuple[Film]): Все фильмы в базе данных.
            user_id (str): Идентификатор пользователя.
            user_ratings (list): Список кортежей с оценками пользователя(film_id, rating).

        Returns:
            set[int]: Множество идентификаторов рекомендованных фильмов.
        """
        
        try:
        
            user_high_rated_films = await self._get_user_high_rated_films(user_ratings)
            target_genres_coefficients = await self._get_most_common_genres(user_high_rated_films, all_films)

            if not target_genres_coefficients:
                
                num_additional_films = num_films
                random_films = set()
                random_films = await self._get_additional_films(random_films, num_additional_films, user_ratings, all_films)
                
                return random_films
            
            suitable_films = await self._get_suitable_films(user_ratings, all_films)
            similar_films = set()
            for film in suitable_films:

                if len(similar_films) >= num_films:
                    break
                
                is_similar = await self._get_similar_film(film, target_genres_coefficients)
                if is_similar:
                    similar_films.add(is_similar)
                    

            if len(similar_films) < num_films:
                num_additional_films = num_films - len(similar_films)
                similar_films = await self._get_additional_films(similar_films, num_additional_films, user_ratings, all_films)
                
            return similar_films  
        
        except Exception as e:
            print(f"Error in _get_recommended_film: {e}")
            raise 
            
    
    async def _get_additional_films(self, similar_films: set, num_additional_films: int, user_ratings: list, all_films: tuple[Film]) -> set:
        
        """
        Добавляет дополнительные случайные фильмы к списку рекомендаций.

        Args:
            similar_films (set): Множество рекомендованных фильмов.
            user_id (str): Идентификатор пользователя.
            num_additional_films (int): Количество дополнительных фильмов для рекомендации.
            user_ratings (list): Список кортежей с оценками пользователя(film_id, rating).

        Returns:
            set: Обновленное множество рекомендаций с добавленными случайными фильмами.
        """

        additional_films = await self._get_random_related_films(num_additional_films, all_films, user_ratings)
        similar_films.update(additional_films)
        
        return similar_films
    
    async def _get_similar_film(self, film: Film, target_genres_coefficients: dict) -> Film | None:
        """
        Определяет и добавляет схожие фильмы с жанрами наподобие предпочитаемых жанров пользователя.

        Args:
            film (Film): Фильм, для которого определяется похожесть на жанры.
            target_genres_coefficients (dict): Словарь коэффициентов заинтересованности в жанрах пользователя.

        Returns:
            Film or None: Фильм, если он похож на предпочитаемые жанры, или None, если не похож.
        """
        try:
            film_genres_coefficient_sum = sum(target_genres_coefficients.get(genre, 0) for genre in film.genres)
            if film_genres_coefficient_sum >= float(SIMILARITY_COEFFICIENT):
                return film

        except Exception as e:
            print(f"Error in _get_similar_film: {e}")
            raise

    async def get_recommendations(self, user_id: str, num_films: int) -> list[Film]:
        
        """
        Генерирует рекомендации фильмов для пользователя.

        Args:
            user_id (str): Идентификатор пользователя.
            num_films (int): Количество фильмов для рекомендации.

        Returns:
            List[Film]: Список рекомендованных фильмов.
        """
        
        try: 
            
            all_films = tuple(await FilmDAO.find_all(self.db))
            user_ratings = await self._get_recent_ratings(user_id=user_id)     
            recommendations = await self._get_recommended_films(num_films, all_films, user_ratings)
            
            return recommendations
        
        except Exception as e:
            logger.opt(exception=e).critical("Error in get_recommendations")
            raise


class DatabaseManager:
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.recommendations = Recommendations(db)
    