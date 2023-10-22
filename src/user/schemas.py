from datetime import datetime

from pydantic import BaseModel, constr
from typing import List, Optional


# Базовая схема для Review
class ReviewBase(BaseModel):
    title: str
    film_id: int
    message: str
    rating: float
    likes: int = 0
    dislikes: int = 0


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
    
    
# Базовая схема для Comment    
class CommentBase(BaseModel):
    message: str
    parent_comment_id: Optional[int] = None


# Схема для создания записи (CRUD - Create)
class CommentCreate(CommentBase):
    pass

# Схема для создания записи (CRUD - Create)
class CommentCreateDB(CommentBase):
    user_id: str
    username: str

# Схема для чтения (CRUD - Read)
class CommentRead(CommentBase):
    id: int

# Схема для обновления записи (CRUD - Update)
class CommentUpdate(BaseModel):
    message: Optional[str] = None