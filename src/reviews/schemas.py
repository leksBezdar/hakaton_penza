from pydantic import BaseModel, constr


attitude_pattern = '^(positive|negative|neutral)$'


# Базовая схема для Review
class ReviewBase(BaseModel):
    title: str
    film_id: int
    message: str
    attitude: constr(pattern=attitude_pattern) | None
    liked_by_users: list = []
    disliked_by_users: list = []


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
    title: str | None
    message: str | None
    attitude: constr(pattern=attitude_pattern) | None
    liked_by_users: list | None  
    disliked_by_users: list | None 
    