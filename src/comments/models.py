from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from ..database import Base

    
class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    film_id: Mapped[int] = mapped_column(ForeignKey("films.id", ondelete="CASCADE"), nullable=True)
    username: Mapped[str] = mapped_column(ForeignKey("users.username", ondelete="CASCADE"))
    message: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True),
                                                 server_default=func.now())
    parent_review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"), nullable=True)
    parent_comment_id: Mapped[int] = mapped_column(ForeignKey("comments.id"), nullable=True)