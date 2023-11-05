from typing import List

from fastapi import APIRouter, Depends, Request, Response

from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas

from .dependencies import get_current_user
from .models import User
from .service import DatabaseManager
from ..database import get_async_session


router = APIRouter()


@router.post("/registration/", response_model=schemas.User)
async def create_user(
    user_data: schemas.UserCreate,
    db: AsyncSession = Depends(get_async_session),
) -> User:

    db_manager = DatabaseManager(db)
    user_crud = db_manager.user_crud

    return await user_crud.create_user(user=user_data)


@router.post("/login/")
async def login(
    response: Response,
    username: str,
    password: str,
    isDev: bool = False,
    db: AsyncSession = Depends(get_async_session),
):
    db_manager = DatabaseManager(db)
    user_crud = db_manager.user_crud
    token_crud = db_manager.token_crud

    user = await user_crud.authenticate_user(username=username, password=password)
    token = await token_crud.create_tokens(user_id=user.id, response=response, isDev=isDev)

    return token, user.id


@router.post("/logout/")
async def logout(
    request: Request,
    response: Response,
    db: AsyncSession = Depends(get_async_session),
):
    db_manager = DatabaseManager(db)
    user_crud = db_manager.user_crud

    await user_crud.logout(refresh_token=request.cookies.get('refresh_token'))

    return response


@router.get("/me", response_model=schemas.User)
async def get_me(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
) -> User | None:

    db_manager = DatabaseManager(db)
    user_crud = db_manager.user_crud

    user = await user_crud.get_existing_user(username=current_user.username)

    return user


@router.get("/get_user", response_model=None)
async def get_user(
    token: str = None,
    username: str = None,
    email: str = None,
    user_id: str = None,
    db: AsyncSession = Depends(get_async_session),
) -> User | None:

    db_manager = DatabaseManager(db)
    user_crud = db_manager.user_crud

    user = await user_crud.get_existing_user(token=token, username=username, email=email, user_id=user_id)

    return user


@router.get("/get_all_users", response_model=List[schemas.User])
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

    new_token = await token_crud.refresh_token(request.cookies.get("refresh_token"), response=response)

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

    response = await user_crud.abort_user_sessions(username=username, email=email, user_id=user_id)

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

    response = await user_crud.delete_user(username=username, email=email, user_id=user_id)

    return response
