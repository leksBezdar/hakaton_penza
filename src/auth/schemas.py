from pydantic import BaseModel, EmailStr, Field, validator
from typing import List

from .config import (
    MIN_USERNAME_LENGTH as user_min_len,
    MAX_USERNAME_LENGTH as user_max_len,
    MIN_PASSWORD_LENGTH as pass_min_len,
    MAX_PASSWORD_LENGTH as pass_max_len,
                    )

class UserBase(BaseModel):
    email: EmailStr
    username: str
    is_superuser: bool = Field(False)
    postponed_films: List = []
    planned_films: List = []
    abandoned_films: List = []
    favorite_films: List = []
    finished_films: List = []
    

class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str
    
        
    @validator("username")
    def validate_username_length(cls, value):
        if len(value) < int(user_min_len) or len(value) > int(user_max_len):
            raise ValueError("Username must be between 3 and 15 characters")
        
        return value
    
    @validator("password")
    def validate_password_complexity(cls, value):
        if len(value) < int(pass_min_len) or len(value) > int(pass_max_len):
            raise ValueError("Password must be between 3 and 30 characters")
        
        return value
    
class UserUpdate(UserBase):
    email: EmailStr | None
    password: str | None
        

class User(UserBase):
    id: str
    
    class Config:
        from_attributes = True
    
class UserCreateDB(UserBase):
    id: str
    hashed_password: str | None
       
    
class RefreshTokenCreate(BaseModel):
    refresh_token: str
    expires_at: int
    user_id: str

class RefreshTokenUpdate(RefreshTokenCreate):
    user_id: str | None
    
class Token(BaseModel):
    access_token: str
    refresh_token: str
