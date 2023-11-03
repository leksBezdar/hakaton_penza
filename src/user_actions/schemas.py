from pydantic import BaseModel

from typing import List

class UserFilmRatingCreate(BaseModel):
    user_id: str
    film_id: int
    rating: float

class UserFilmRatingUpdate(BaseModel):
    rating: float

class UserFilmRatingRead(UserFilmRatingCreate):
    id: int

class UserFilmRatingDelete(BaseModel):
    id: int

class UserFilmRatingList(BaseModel):
    items: List[UserFilmRatingRead]