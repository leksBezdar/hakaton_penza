from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from ..database import Base


class UserFilmRating(Base):
    __tablename__ = 'user_film_ratings'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"))
    film_id: Mapped[int] = mapped_column(
        ForeignKey("films.id", ondelete="CASCADE"))
    rating: Mapped[float] = mapped_column(nullable=False)
