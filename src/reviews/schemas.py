from pydantic import BaseModel
from typing import Optional


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
    username: str
    user_id: str

# Схема для чтения (CRUD - Read)
class ReviewRead(ReviewBase):
    id: int

# Схема для обновления записи (CRUD - Update)
class ReviewUpdate(BaseModel):
    title: Optional[str] = None
    message: Optional[str] = None
    rating: Optional[float] = None
    likes: Optional[int] = None
    dislikes: Optional[int] = None
    