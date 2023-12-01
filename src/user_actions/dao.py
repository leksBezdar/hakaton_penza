from .models import UserFilmRating
from .schemas import UserFilmRatingCreate, UserFilmRatingUpdate

from ..dao import BaseDAO


class UserFilmRatingDAO(BaseDAO[UserFilmRating, UserFilmRatingCreate, UserFilmRatingUpdate]):
    model = UserFilmRating
