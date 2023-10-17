from datetime import datetime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ARRAY, TIMESTAMP, Float, Integer, Boolean, ForeignKey, JSON, String

from ..database import Base

class Film(Base):
    __tablename__ = "films"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    poster: Mapped[str] = mapped_column(nullable=False, unique=True)
    trailer: Mapped[str] = mapped_column(nullable=True, unique=True)
    created_at: Mapped[int] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    genres: Mapped[list] = mapped_column(ARRAY(String), nullable=False, default=[])
    year: Mapped[int] = mapped_column(nullable=False)
    director: Mapped[str] = mapped_column(nullable=False)
    writers: Mapped[list] = mapped_column(ARRAY(String), default=[], nullable=False)
    producers: Mapped[list] = mapped_column(ARRAY(String), default=[], nullable=False)
    cinematographers: Mapped[list] = mapped_column(ARRAY(String), default=[], nullable=False)
    composers: Mapped[list] = mapped_column(ARRAY(String), default=[], nullable=False)
    art_directors: Mapped[list] = mapped_column(ARRAY(String), default=[], nullable=False)
    editor: Mapped[list] = mapped_column(ARRAY(String), default=[], nullable=False)
    budget: Mapped[str] = mapped_column(nullable=False)
    box_office_world: Mapped[str] = mapped_column(nullable=False)
    premiere_russia: Mapped[str] = mapped_column(nullable=True)
    premiere_world: Mapped[str] = mapped_column(nullable=False)
    age_rating: Mapped[str] = mapped_column(nullable=False)
    
    average_rating: Mapped[float] = mapped_column(nullable=True)
