from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from ..database import Base

    
class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[str] = mapped_column(primary_key=True, nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(nullable=False)
    film_id: Mapped[int] = mapped_column(ForeignKey("films.id", ondelete="CASCADE"), nullable=True)
    username: Mapped[str] = mapped_column(nullable=False)
    message: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                 server_default=func.now())
    
class ReplyComment(Base):
    __tablename__ = "reply_comments"
    
    id: Mapped[str] = mapped_column(primary_key=True)
    comment_id: Mapped[str] = mapped_column(ForeignKey('comments.id', ondelete="CASCADE"))
    parent_comment_id: Mapped[str] = mapped_column(ForeignKey('comments.id', ondelete="CASCADE"))
    parent_review_id: Mapped[int] = mapped_column(ForeignKey('reviews.id', ondelete="CASCADE"))