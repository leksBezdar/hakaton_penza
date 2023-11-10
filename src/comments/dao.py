from .models import Comment, ReplyComment
from .schemas import CommentCreate, CommentUpdate, ReplyCommentUpdate, ReplyCommentCreate

from ..dao import BaseDAO

    
class CommentDAO(BaseDAO[Comment, CommentCreate, CommentUpdate]):
    model = Comment

class ReplyCommentDAO(BaseDAO[ReplyComment, ReplyCommentCreate, ReplyCommentUpdate]):
    model = ReplyComment