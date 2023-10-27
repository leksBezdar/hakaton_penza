from pydantic import BaseModel, constr
from typing import List, Optional


# Базовая схема для Film
class FilmBase(BaseModel):
    title: str
    poster: str
    trailer: Optional[str] = None
    country: str
    genres: List[str]
    year: int
    director: Optional[str] = None
    writers: Optional[List[str]] = None
    producers: Optional[List[str]] = None
    cinematographers: Optional[List[str]] = None
    composers: Optional[List[str]] = None
    art_directors: Optional[List[str]] = None
    editor: Optional[List[str]] = None
    budget: Optional[str] = None
    box_office_world: Optional[str] = None
    premiere_russia: Optional[str] = None
    premiere_world: str
    average_rating: float
    age_rating: Optional[str] = None


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
    average_rating: Optional[float]

# Схема для обновления записи (CRUD - Update)
class FilmUpdate(FilmBase):
    title: Optional[str] = None
    poster: Optional[str] = None
    trailer: Optional[str] = None
    country: Optional[str] = None
    genres: Optional[List[str]] = None
    year: Optional[int] = None
    director: Optional[str] = None
    writers: Optional[List[str]] = None
    producers: Optional[List[str]] = None
    cinematographers: Optional[List[str]] = None
    composers: Optional[List[str]] = None
    art_directors: Optional[List[str]] = None
    editor: Optional[List[str]] = None
    budget: Optional[str] = None
    box_office_world: Optional[str] = None
    premiere_russia: Optional[str] = None
    premiere_world: Optional[str] = None
    age_rating: Optional[str] = None
    average_rating: Optional[float] = None
