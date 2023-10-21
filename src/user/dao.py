from .models import Comment, Review
from .schemas import CommentCreate, CommentUpdate, ReviewCreate, ReviewUpdate

from ..dao import BaseDAO


class ReviewDAO(BaseDAO[Review, ReviewCreate, ReviewUpdate]):
    model = Review
    
    
class CommentDAO(BaseDAO[Comment, CommentCreate, CommentUpdate]):
    model = Comment
