from pydantic import BaseModel, constr
from typing import List, Optional


# Базовая схема для Review
class ReviewBase(BaseModel):
    title: str
    film_id: int
    message: str
    rating: float


# Схема для создания записи (CRUD - Create)
class ReviewCreate(ReviewBase):
    pass

# Схема для создания записи (CRUD - Create)
class ReviewCreateDB(ReviewBase):
    user_id: str

# Схема для чтения (CRUD - Read)
class ReviewRead(ReviewBase):
    id: int

# Схема для обновления записи (CRUD - Update)
class ReviewUpdate(ReviewBase):
    title: Optional[str] = None
    user_id: Optional[str] = None
    film_id: Optional[int] = None
    message: Optional[str] = None
    rating: Optional[float] = None