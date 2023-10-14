from .models import Film
from .schemas import FilmCreate, FilmUpdate

from ..dao import BaseDAO


    
class FilmDAO(BaseDAO[Film, FilmCreate, FilmUpdate]):
    model = Film
    