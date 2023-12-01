from datetime import datetime
from typing import Annotated

from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, JSON, String
from sqlalchemy.orm import  Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY


from ..database import Base

user_list = Annotated[list, mapped_column(ARRAY(JSON), nullable=False, default=[])]

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_superuser: Mapped[bool] = mapped_column(nullable=False, default=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    planned_films: Mapped[user_list]
    postponed_films: Mapped[user_list]
    abandoned_films: Mapped[user_list]
    favorite_films: Mapped[user_list]
    finished_films: Mapped[user_list]


class Refresh_token(Base):
    __tablename__ = 'refresh_tokens'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    refresh_token: Mapped[str] = mapped_column(index=True)
    expires_at: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
