from typing import List
from random import sample
from sqlalchemy import select

from loguru import logger

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..films.dao import FilmDAO
from ..films.models import Film
from ..user_actions.models import UserFilmRating

from .config import SIMILARITY_COEFFICIENT
from .config import THRESHOLD_FOR_POSITIVE_RATING

class Recommendations:
    
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def _get_recent_ratings(self, user_id: str, limit: int = 20) -> list[tuple[int, float]]:
    
        try:
            query = (
                select(UserFilmRating.film_id, UserFilmRating.rating)
                .where(UserFilmRating.user_id == user_id)
                .order_by(UserFilmRating.id.desc())
                .limit(limit)
            )
                
            result = await self.db.execute(query)            
            rows = result.fetchall()

            user_ratings = [(row[0], row[1]) for row in rows]
            
            return user_ratings
        
        except Exception as e:
            logger.opt(exception=e).critical("Error in _get_recent_ratings")
            raise

    async def _get_random_related_films(self, user_id: str, count: int) -> List[int]:
        
        try:
            all_films = await FilmDAO.find_all(self.db)
            
            user_ratings = await self._get_recent_ratings(user_id=user_id)
            suitable_films = await self._get_suitable_films(user_ratings, all_films)

            if len(suitable_films) <= count:
                random_unrelated_films = suitable_films
            else:
                random_unrelated_films = sample(suitable_films, count)

            return random_unrelated_films
        except Exception as e:
            logger.opt(exception=e).critical("Error in _get_random_related_films")
            raise
        
    @staticmethod
    async def _get_user_positive_ratings(user_ratings: list) -> list[int]:
        
        return [film_id for film_id, rating in user_ratings if rating >= float(THRESHOLD_FOR_POSITIVE_RATING)]
    
    @staticmethod
    async def _get_user_negative_ratings(user_ratings: list) -> list[int]:
        
        return [film_id for film_id, rating in user_ratings if rating < float(THRESHOLD_FOR_POSITIVE_RATING)]
    
    async def _get_suitable_films(self, user_ratings: list, all_films: list[Film]) -> list[int]:
            
        user_positive_ratings = await self._get_user_positive_ratings(user_ratings)
        user_negative_ratings = await self._get_user_negative_ratings(user_ratings)
                
        user_rated_films = user_positive_ratings + user_negative_ratings
        suitable_films = [film.id for film in all_films if film.id not in user_rated_films]
        
        return suitable_films
    
    async def _get_most_common_genres(self, user_positive_ratings: list, num_genres: int) -> list[str]:
        
        genre_count = {}
        for film_id in user_positive_ratings:
            film = await FilmDAO.find_one_or_none(self.db, Film.id == film_id)
            for genre in film.genres:
                genre_count[genre] = genre_count.get(genre, 0) + 1

        sorted_genres = sorted(genre_count.keys(), key=lambda genre: genre_count[genre], reverse=True)
        
        return sorted_genres[:num_genres]

    async def _get_recommended_film_ids(self, num_films: int, user_id: str, num_genres: int) -> list[int]:
        user_ratings = await self._get_recent_ratings(user_id=user_id)
        user_positive_ratings = await self._get_user_positive_ratings(user_ratings)

        if not user_positive_ratings:
            return await self._get_random_related_films(user_id, num_films)
    
        user_positive_genres = await self._get_most_common_genres(user_positive_ratings, num_genres)
        
        similar_films = set()
        for film_id in user_positive_ratings:
            film = await FilmDAO.find_one_or_none(self.db, Film.id == film_id)
            
            similar_films.update(await self._get_similar_films(film, user_positive_genres, num_films))
                                    
        recommendations = list(set(similar_films) - set(user_positive_ratings))
        
        if len(recommendations) < num_films:
            additional_count = num_films - len(recommendations)
            recommendations = await self._get_additional_films(recommendations, user_id, additional_count)
        
        return recommendations

    async def _get_additional_films(self, recommendations: list, user_id: str, additional_count: int) -> list:
        
        random_unrelated_films = await self._get_random_related_films(user_id, additional_count)
        recommendations.extend(random_unrelated_films)
        
        return recommendations

    async def _get_similar_films(self, film: Film, user_positive_genres: list, num_films: int) -> set:
        
        similar_films = set()
        all_films = await FilmDAO.find_all(self.db)
                
        for other_film in all_films:
            
            if other_film.id != film.id:
                common_genres = set(other_film.genres) & set(user_positive_genres)
                similarity = len(common_genres) / len(user_positive_genres)
                if similarity >= float(SIMILARITY_COEFFICIENT):
                    print(similarity)
                    similar_films.add(other_film.id)
                    if len(similar_films) >= num_films:
                        break
        print(similar_films)
        return similar_films

    async def get_recommendations(self, user_id: str, num_films: int, num_genres: int) -> List[Film]:
        try: 
            recommendations = await self._get_recommended_film_ids(num_films, user_id, num_genres)
            recommended_films = [await FilmDAO.find_one_or_none(self.db, Film.id == film_id) for film_id in recommendations]

            return recommended_films
        
        except Exception as e:
            logger.opt(exception=e).critical("Error in get_recommendations")
            raise

class DatabaseManager:
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.recommendations = Recommendations(db)
