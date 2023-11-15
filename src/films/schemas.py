from pydantic import BaseModel
from typing import List


# Базовая схема для Film
class FilmBase(BaseModel):
    title: str
    poster: str
    trailer: str | None = None
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
    premiere_world: str | None = None
    average_rating: float = 0
    age_rating: str | None
    local_rating: float = 0
    description: str | None = None


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

