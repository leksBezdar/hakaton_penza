from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from . import exceptions
from .utils import OAuth2PasswordBearerWithCookie
from .service import DatabaseManager
from .models import User

from ..database import get_async_session
from ..utils import check_record_existence



async def get_current_user(
        request: Request,
        db: AsyncSession = Depends(get_async_session),
):

    db_manager = DatabaseManager(db)
    token_crud = db_manager.token_crud

    try:
        user_id = await token_crud.get_access_token_payload(request.cookies.get('access_token'))

    except KeyError:
        raise exceptions.InvalidCredentials

    user = await check_record_existence(db, User, user_id)
    return user
