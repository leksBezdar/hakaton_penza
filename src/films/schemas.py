from pydantic import BaseModel, constr
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
    average_rating: float

    age_rating: constr(
        pattern='^(G|P|PG13|R|NC17)$'
    )


# Схема для создания записи (CRUD - Create)
class FilmCreate(FilmBase):
    pass


# Схема для чтения (CRUD - Read)
class FilmRead(FilmBase):
    id: int
    average_rating: Optional[float]


# Схема для обновления записи (CRUD - Update)
class FilmUpdate(FilmBase):
    title: Optional[str] = None
    poster: Optional[str] = None
    trailer: Optional[str] = None
    created_at: Optional[int] = None
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

    average_rating: Optional[float] = None


# Схема для удаления записи (CRUD - Delete)
class FilmDelete(BaseModel):
    id: int
