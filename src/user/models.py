from datetime import datetime

from sqlalchemy import ARRAY, TIMESTAMP, Float, Integer, Boolean, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.sql import func

from ..database import Base


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    username: Mapped[str] = mapped_column(ForeignKey("users.username", ondelete="CASCADE"))
    film_id: Mapped[str] = mapped_column(ForeignKey("films.id", ondelete="CASCADE"))
    message: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False)
    likes: Mapped[int] = mapped_column(nullable=False, default=0)
    dislikes: Mapped[int] = mapped_column(nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                 server_default=func.now())
    
    
class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    username: Mapped[str] = mapped_column(ForeignKey("users.username", ondelete="CASCADE"))
    message: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                 server_default=func.now())
    parent_comment_id: Mapped[int] = mapped_column(ForeignKey("comments.id"))