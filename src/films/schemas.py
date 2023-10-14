from pydantic import BaseModel
from typing import List, Optional


# Базовая схема для Film
class FilmBase(BaseModel):
    title: str
    poster: str
    trailer: str
    created_at: int
    country: str
    genres: List[str]
    year: int
    director: str
    writers: List[str]
    producers: List[str]
    cinematographers: List[str]
    composers: List[str]
    art_directors: List[str]
    editor: List[str]
    budget: str
    box_office_world: str
    premiere_russia: Optional[str]
    premiere_world: str
    age_rating: str


# Схема для создания записи (CRUD - Create)
class FilmCreate(FilmBase):
    pass


# Схема для чтения (CRUD - Read)
class FilmRead(FilmBase):
    id: int
    average_rating: Optional[float]


# Схема для обновления записи (CRUD - Update)
class FilmUpdate(FilmBase):
    average_rating: Optional[float]


# Схема для удаления записи (CRUD - Delete)
class FilmDelete(BaseModel):
    id: int