from pydantic import BaseModel

    
# Базовая схема для Comment    
class CommentBase(BaseModel):
    message: str
    parent_review_id: int | None = None
    parent_comment_id: int | None = None
    film_id: int | None = None


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
    message: str | None