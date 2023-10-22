from pydantic import BaseModel
from typing import Optional

    
# Базовая схема для Comment    
class CommentBase(BaseModel):
    message: str
    parent_comment_id: Optional[int] = None


# Схема для создания записи (CRUD - Create)
class CommentCreate(CommentBase):
    pass

# Схема для создания записи (CRUD - Create)
class CommentCreateDB(CommentBase):
    film_id: int
    user_id: str
    username: str

# Схема для чтения (CRUD - Read)
class CommentRead(CommentBase):
    id: int

# Схема для обновления записи (CRUD - Update)
class CommentUpdate(BaseModel):
    message: Optional[str] = None