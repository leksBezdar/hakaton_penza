from pydantic import BaseModel

    
# Базовая схема для Comment    
class CommentBase(BaseModel):
    message: str
    film_id: int | None = None


# Схема для создания записи (CRUD - Create)
class CommentCreate(CommentBase):
    token: str = None
    parent_comment_id: str | None = None
    parent_review_id: int | None = None

# Схема для создания записи (CRUD - Create)
class CommentCreateDB(CommentBase):
    id: str
    user_id: str 
    username: str 

# Схема для чтения (CRUD - Read)
class CommentRead(CommentBase):
    id: str

# Схема для обновления записи (CRUD - Update)
class CommentUpdate(BaseModel):
    message: str | None

   
class ReplyCommentBase(BaseModel):
    comment_id: str 
    parent_comment_id: str | None 
    parent_review_id: int | None 
     
class ReplyCommentCreate(ReplyCommentBase):
    pass

class ReplyCommentCreateDB(ReplyCommentBase):
    id: str

class ReplyCommentUpdate(ReplyCommentBase):
    comment_id: str | None
    parent_comment_id: str | None
    parent_review_id: int | None

class ReplyCommentData(BaseModel):
    comment_id: str
    parent_comment_id: str | None = None
    parent_review_id: int | None = None
    
class ReplyCommentRead(ReplyCommentBase):
    pass
