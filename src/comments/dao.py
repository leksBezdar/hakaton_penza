from .models import Comment
from .schemas import CommentCreate, CommentUpdate

from ..dao import BaseDAO

    
class CommentDAO(BaseDAO[Comment, CommentCreate, CommentUpdate]):
    model = Comment
