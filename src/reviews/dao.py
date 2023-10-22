from .models import Review
from .schemas import ReviewCreate, ReviewUpdate

from ..dao import BaseDAO


class ReviewDAO(BaseDAO[Review, ReviewCreate, ReviewUpdate]):
    model = Review
    