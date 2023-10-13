from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from .utils import OAuth2PasswordBearerWithCookie

from . import exceptions
from .models import User
from ..database import get_async_session
from .service import DatabaseManager


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/auth/login")


async def get_current_user(
        db: AsyncSession = Depends(get_async_session),
        token: str = Depends(oauth2_scheme),
):
    
    db_manager = DatabaseManager(db)
    user_crud = db_manager.user_crud
    token_crud = db_manager.token_crud
    
    try:
        user_id = await token_crud.get_access_token_payload(token)

    except KeyError:
        raise exceptions.InvalidCredentials
    
    user = await user_crud.get_existing_user(user_id=user_id)
    return user
    
        
    
