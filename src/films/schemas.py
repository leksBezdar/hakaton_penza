from pydantic import BaseModel, constr
from typing import List


# Базовая схема для Film
class FilmBase(BaseModel):
    title: str
    poster: str
    trailer: str | None
    country: str
    genres: List[str]
    year: int
    director: str | None
    writers: List[str] | None
    producers: List[str] | None
    cinematographers: List[str] | None
    composers: List[str] | None
    art_directors: List[str] | None
    editor: List[str] | None
    budget: str | None
    box_office_world: str | None
    premiere_russia: str | None
    premiere_world: str
    average_rating: float
    age_rating: str | None
    local_rating: float 


# Схема для создания записи (CRUD - Create)
class FilmCreate(FilmBase):
    is_planned: bool  = False
    is_abandoned: bool  = False
    is_favorite: bool  = False
    is_postponed: bool  = False
    is_finished: bool  = False

# Схема для чтения (CRUD - Read)
class FilmRead(FilmBase):
    id: int
    average_rating: float | None
    local_rating: float | None

# Схема для обновления записи (CRUD - Update)
class FilmUpdate(FilmBase):
    title: str | None
    poster: str | None
    trailer: str | None
    country: str | None
    genres: List[str] | None
    year: int | None
    director: str | None
    writers: List[str] | None
    producers: List[str] | None
    cinematographers: List[str] | None
    composers: List[str] | None
    art_directors: List[str] | None
    editor: List[str] | None
    budget: str | None
    box_office_world: str | None
    premiere_russia: str | None
    premiere_world: str | None
    age_rating: str | None
    average_rating: float | None
    

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

