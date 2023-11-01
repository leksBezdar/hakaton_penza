from .models import Film, UserFilmRating
from .schemas import FilmCreate, FilmUpdate, UserFilmRatingCreate, UserFilmRatingUpdate

from ..dao import BaseDAO


class FilmDAO(BaseDAO[Film, FilmCreate, FilmUpdate]):
    model = Film
    

class UserFilmRatingDAO(BaseDAO[UserFilmRating, UserFilmRatingCreate, UserFilmRatingUpdate]):
    model = UserFilmRating
