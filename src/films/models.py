from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ARRAY, String

from ..database import Base


class Film(Base):
    __tablename__ = "films"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    poster: Mapped[str] = mapped_column(nullable=False, unique=True)
    trailer: Mapped[str] = mapped_column(nullable=True, unique=True)
    country: Mapped[str] = mapped_column(nullable=False)
    genres: Mapped[list] = mapped_column(ARRAY(String), nullable=False, default=[])
    year: Mapped[int] = mapped_column(nullable=False)
    director: Mapped[str] = mapped_column(nullable=True)
    writers: Mapped[list] = mapped_column(ARRAY(String), default=[], nullable=True)
    producers: Mapped[list] = mapped_column(ARRAY(String), default=[], nullable=True)
    cinematographers: Mapped[list] = mapped_column(ARRAY(String), default=[], nullable=True)
    composers: Mapped[list] = mapped_column(ARRAY(String), default=[], nullable=True)
    art_directors: Mapped[list] = mapped_column(ARRAY(String), default=[], nullable=True)
    editor: Mapped[list] = mapped_column(ARRAY(String), default=[], nullable=True)
    budget: Mapped[str] = mapped_column(nullable=True)
    box_office_world: Mapped[str] = mapped_column(nullable=True)
    premiere_russia: Mapped[str] = mapped_column(nullable=True)
    premiere_world: Mapped[str] = mapped_column(nullable=False)
    age_rating: Mapped[str] = mapped_column(nullable=False, default=False)
    is_planned: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_abandoned: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_favorite: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_postponed: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_finished: Mapped[bool] = mapped_column(nullable=False, default=False)

    average_rating: Mapped[float] = mapped_column(nullable=True)
