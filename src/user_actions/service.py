from sqlalchemy.ext.asyncio import AsyncSession

from ..reviews.dao import ReviewDAO
from ..reviews.models import Review

from ..auth.models import User
from ..auth.dao import UserDAO
from ..auth.service import DatabaseManager as AuthManager

from ..films.models import Film
from ..films.dao import FilmDAO

from ..utils import check_record_existence

from .dao import UserFilmRatingDAO
from .models import UserFilmRating

from . import schemas
from . import exceptions


class UserFilmCRUD:
    
    def __init__(self, db: AsyncSession):
        self.db = db 
        self.LIST_TYPES = {
            "favorite": "favorite_films",
            "postponed": "postponed_films",
            "abandoned": "abandoned_films",
            "planned": "planned_films",
            "finished": "finished_films",
        }


    async def update_user_list(self, token: str, film_id: int, list_type: str) -> str:

        auth_manager = AuthManager(self.db)
        token_crud = auth_manager.token_crud

        user_id = await token_crud.get_access_token_payload(access_token=token)

        film = await check_record_existence(db=self.db, model=Film, record_id=film_id)
        user = await check_record_existence(self.db, User, user_id)
        
        user_list_attribute = self.LIST_TYPES.get(list_type)
        
        if not user_list_attribute:
            raise exceptions.InvalidListType
        
        return await self._update_user_list(user, user_list_attribute, film)

    @staticmethod
    async def _create_film_data(film: Film) -> dict:
        return {
            "id": film.id, "title": film.title, "poster": film.poster,
            "rating": film.average_rating, "genres": film.genres
        }


    async def _update_user_list(self, user: User, user_list_attribute: str, film: Film) -> str:
        
        film_data = await self._create_film_data(film=film)
        
        # Получаем текущий список пользователя, который пользователь хочет обновить
        target_user_list = getattr(user, user_list_attribute, [])
        
        if user_list_attribute != "favorite_films":
            
            await self._check_other_user_lists(
                film_data=film_data,
                user=user,
                user_list_attribute=user_list_attribute
            )
        
        await self._toggle_film_data_in_user_list(target_user_list=target_user_list, film_data=film_data)
        await self._update_user_in_database(user, user_list_attribute, target_user_list) 

        return {"Message": "Update was successful"}
    
    
    @staticmethod
    async def _toggle_film_data_in_user_list(target_user_list: list, film_data: dict):
        
        if film_data in target_user_list:
            target_user_list.remove(film_data)
        else:
            target_user_list.append(film_data)
    
    
    async def _check_other_user_lists(self, film_data: dict, user: User, user_list_attribute: str) -> None:     
                
        # Проверка, что film_id не находится в других списках и не является записью в списке favorite_films
        other_list_attributes = [key for key in self.LIST_TYPES.values()if key != user_list_attribute and key != "favorite_films"]
 
        for other_list_attribute in other_list_attributes:
            
            other_list = getattr(user, other_list_attribute, [])
            
            if film_data in other_list:         
                other_list.remove(film_data)
                
                await self._update_user_in_database(user, other_list_attribute, other_list) 
                
            
    async def _update_user_in_database(self, user: User, user_list_attribute: str, target_user_list: list) -> None:
        
        user_update_data = {user_list_attribute: target_user_list}
        user_update = await UserDAO.update(self.db, User.id == user.id, obj_in=user_update_data)

        self.db.add(user_update)
        await self.db.commit()
        await self.db.refresh(user_update)
    
    
    async def rate_the_film(self, rating_data: schemas.UserFilmRatingCreate):
        
        user_id = rating_data.user_id
        film_id = rating_data.film_id
        
        existing_rating = await self._get_existing_rating(user_id, film_id)

        if existing_rating:
            await self._delete_existing_rating(existing_rating)
            
        await self._create_new_rating(rating_data)       
        return await self._update_average_local_rating(film_id)

    async def _get_existing_rating(self, user_id, film_id) -> UserFilmRating:
        return await UserFilmRatingDAO.find_one_or_none(self.db, UserFilmRating.user_id == user_id, UserFilmRating.film_id == film_id)

    async def _delete_existing_rating(self, existing_rating: UserFilmRating):
        await UserFilmRatingDAO.delete(self.db, UserFilmRating.id == existing_rating.id)

    async def _create_new_rating(self, rating_data: schemas.UserFilmRatingCreate):
        new_rating = await UserFilmRatingDAO.add(
            self.db, 
            schemas.UserFilmRatingCreate(
            **rating_data.model_dump()
        ))
        self.db.add(new_rating)
        await self.db.commit()
        await self.db.refresh(new_rating)
        return new_rating
    
    async def _update_average_local_rating(self, film_id: int):
        
        new_rating = await self._get_average_local_rating(film_id)
        obj_in = {"local_rating": new_rating}
        
        await FilmDAO.update(
            self.db,    
            Film.id == film_id,
            obj_in=obj_in)

        await self.db.commit()

        return {"Message": "The evaluation was successful"}
         
    
    async def _get_average_local_rating(self, film_id: int) -> float:
        
        films = await UserFilmRatingDAO.find_all(self.db, UserFilmRating.film_id == film_id)
        
        ratings = [film.rating for film in films]
        
        return sum(ratings) / len(ratings)
    
    
    async def get_ratings_for_film(self, film_id: int) -> list:
        
        await check_record_existence(self.db, Film, film_id)
        
        ratings = await UserFilmRatingDAO.find_all(self.db, UserFilmRating.film_id == film_id)
        
        rating_dict = {}
        
        for rating in ratings:
            user_id = rating.user_id
            rating_value = rating.rating
            rating_dict[user_id] = rating_value
        
        return rating_dict


class UserReviewCRUD:
    
    def __init__(self, db: AsyncSession):
        self.db = db
        
    
    async def rate_the_review(self, user_id: str, review_id: int, action: str):

        review = await ReviewDAO.find_one_or_none(self.db, Review.id == review_id)

        obj_in = await self._toggle_review_reaction(review, user_id, action)
        review_update = await ReviewDAO.update(self.db, Review.id == review_id, obj_in=obj_in)

        self.db.add(review_update)
        await self.db.commit()
        await self.db.refresh(review_update)

        return review

    async def _toggle_review_reaction(self, review: Review, user_id: str, action: str):
        
        liked_by_users = set(review.liked_by_users)
        disliked_by_users = set(review.disliked_by_users)

        if action == 'like':
            self._handle_like(liked_by_users, disliked_by_users, user_id)
        elif action == 'dislike':
            self._handle_dislike(liked_by_users, disliked_by_users, user_id)
            
        return {
                "liked_by_users": list(liked_by_users),
                "disliked_by_users": list(disliked_by_users),
                "review_rating": await self._get_review_rating(liked_by_users, disliked_by_users)
            }
    
    @staticmethod    
    def _handle_like(liked_by_users: set, disliked_by_users: set, user_id: str):
        
        if user_id in liked_by_users:
            liked_by_users.remove(user_id)
        else:
            liked_by_users.add(user_id)
            disliked_by_users.discard(user_id)
            
    @staticmethod
    def _handle_dislike(liked_by_users: set, disliked_by_users: set, user_id: str):
        
        if user_id in disliked_by_users:
            disliked_by_users.remove(user_id)
        else:
            disliked_by_users.add(user_id)
            liked_by_users.discard(user_id)
        
    async def _get_review_rating(self, review_likes: list, review_dislikes: list):

        return len(review_likes) - len(review_dislikes)
        

class DatabaseManager:
    """
    Класс для управления всеми CRUD-классами и применения изменений к базе данных.

    Args:
        db (AsyncSession): Сессия базы данных SQLAlchemy.

    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_film_crud = UserFilmCRUD(db)
        self.user_review_crud = UserReviewCRUD(db)

    async def commit(self):
        await self.db.commit()
