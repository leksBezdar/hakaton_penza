from .models import User, Refresh_token
from .schemas import RefreshTokenCreate, RefreshTokenUpdate, UserCreateDB, UserUpdate

from ..dao import BaseDAO


class UserDAO(BaseDAO[User, UserCreateDB, UserUpdate]):
    model = User


class RefreshTokenDAO(BaseDAO[Refresh_token, RefreshTokenCreate, RefreshTokenUpdate]):
    model = Refresh_token
