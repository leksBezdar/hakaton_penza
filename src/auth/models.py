from datetime import datetime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import TIMESTAMP, Integer, Boolean, ForeignKey, JSON, String

from ..database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    
    
class Refresh_token(Base):
    __tablename__ = 'refresh_tokens'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    refresh_token: Mapped[str] = mapped_column(String, index=True)
    expires_at: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                 server_default=func.now())
    user_id: Mapped[str] = mapped_column(String, ForeignKey(
        "users.id", ondelete="CASCADE"))
