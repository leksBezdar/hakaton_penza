from pydantic import BaseModel, validator

from typing import List


class UserFilmRatingCreate(BaseModel):
    user_id: str
    film_id: int
    rating: float

    @validator("rating")
    def validate_rating(cls, value):
        if value < 1.0 or value > 10.0:
            raise ValueError("Рейтинг должен быть в диапазоне от 1.0 до 10.0")
        return value


class UserFilmRatingUpdate(BaseModel):
    rating: float


class UserFilmRatingRead(UserFilmRatingCreate):
    id: int


class UserFilmRatingDelete(BaseModel):
    id: int


class UserFilmRatingList(BaseModel):
    items: List[UserFilmRatingRead]
