import pandas as pd

from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from ..films.dao import UserFilmRatingDAO

from ..database import get_async_session

from ..films.service import DatabaseManager as film_manager
from ..auth.service import DatabaseManager as auth_manager


router = APIRouter()


@router.get('/get_matrix')
async def get_matrix(db: AsyncSession = Depends(get_async_session)):
    
    films_manager = film_manager(db)
    users_manager = auth_manager(db)
    
    film_crud = films_manager.film_crud
    user_crud = users_manager.user_crud
    
    films = await film_crud.get_all_films(limit=1000)
    users = await user_crud.get_all_users(limit=1000)
    
    ratings = await UserFilmRatingDAO.find_all(db, limit=1000)
    
    user_ids = [user.id for user in users]
    film_ids = [film.id for film in films]
    
    rating_matrix = pd.DataFrame(index=user_ids, columns=film_ids)
    
    for rating in ratings:
        rating_matrix.at[rating.user_id, rating.film_id] = rating.rating

    rating_matrix = rating_matrix.fillna(0)
    
    
    return rating_matrix.to_json()
