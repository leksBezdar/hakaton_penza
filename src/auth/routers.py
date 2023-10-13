from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from typing import List, Optional

from .config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

from . import schemas

from .dependencies import get_current_user
from .models import User
from .service import DatabaseManager
from ..database import get_async_session


router = APIRouter()


# Регистрация нового пользователя
@router.post("/registration/", response_model=schemas.User)
async def create_user(
    user_data: schemas.UserCreate,
    db: AsyncSession = Depends(get_async_session),
) -> User:
    db_manager = DatabaseManager(db)
    user_crud = db_manager.user_crud
    
    return await user_crud.create_user(user=user_data)


# Точка входа пользователя
@router.post("/login/")
async def login(
    request: Request,
    response: Response,
    credentials: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_session),
):
    
    db_manager = DatabaseManager(db)
    user_crud = db_manager.user_crud
    token_crud = db_manager.token_crud

    user = await user_crud.authenticate_user(username=credentials.username, password=credentials.password)
    
    token = await token_crud.create_tokens(user_id = user.id)
    
    response.set_cookie(
        'access_token',
        token.access_token,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True
    )
    response.set_cookie(
        'refresh_token',
        token.refresh_token,
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        httponly=True
    )
    
    return token



# Точка выхода пользователя
@router.post("/logout/")
async def logout(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_async_session),
):
   
    db_manager = DatabaseManager(db)
    user_crud = db_manager.user_crud
    
    await user_crud.logout(refresh_token=request.cookies.get('refresh_token'))
    
    response = JSONResponse(content={
        "message": "logout successful",
    })
        
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    
    return response


@router.get("/me", response_model=schemas.User)
async def get_current_user(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
) -> Optional[User]:
    
    db_manager = DatabaseManager(db)
    user_crud = db_manager.user_crud
    
    user = await user_crud.get_existing_user(username = current_user.username)
    
    return user


# Получение информации о пользователе по имени пользователя
@router.get("/read_user", response_model=None)
async def get_user(
    username: str = None,
    email: str = None,
    user_id: str = None,
    db: AsyncSession = Depends(get_async_session),
) -> Optional[User]:

    db_manager = DatabaseManager(db)
    user_crud = db_manager.user_crud
    
    user = await user_crud.get_existing_user(username=username, email=email, user_id=user_id)

    return user


# Получение списка всех пользователей
@router.get("/read_all_users", response_model=List[schemas.User])
async def get_all_users(
    offset: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_async_session),
):
    db_manager = DatabaseManager(db)
    user_crud = db_manager.user_crud
    
    return await user_crud.get_all_users(offset=offset, limit=limit)


@router.patch("/refresh_tokens")
async def refresh_token(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_async_session),
):
    
    db_manager = DatabaseManager(db)
    token_crud = db_manager.token_crud
    
    new_token = await token_crud.refresh_token(request.cookies.get("refresh_token"))

    response.set_cookie(
        'access_token',
        new_token.access_token,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
    )
    response.set_cookie(
        'refresh_token',
        new_token.refresh_token,
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        httponly=True,
    )
    
    
    return new_token


@router.delete("/delete_user_sessions")
async def delete_user_sessions(
    username: str = None,
    email: str = None,
    user_id: str = None,
    db: AsyncSession = Depends(get_async_session),
):
    
    db_manager = DatabaseManager(db)
    user_crud = db_manager.user_crud
    
    await user_crud.abort_user_sessions(username=username, email=email, user_id=user_id)
    
    response = JSONResponse(content={
        "message": "Delete successful",
    })
    
    return response


@router.delete("/delete_user")
async def delete_user(
    username: str = None,
    email: str = None,
    user_id: str = None,
    db: AsyncSession = Depends(get_async_session),
):
    
    db_manager = DatabaseManager(db)
    user_crud = db_manager.user_crud
    
    await user_crud.delete_user(username=username, email=email, user_id=user_id)
    
    response = JSONResponse(content={
        "message": "Delete successful",
    })
    
    return response