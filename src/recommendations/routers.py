from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from .service import DatabaseManager


router = APIRouter()


@router.get("/get_recommendations/")
async def get_recommendations(
    user_id: str,
    num_films: int = 20,
    num_genres: int = 10,
    db: AsyncSession = Depends(get_async_session)):
    try:
        
        db_manager = DatabaseManager(db)
        recommendations = db_manager.recommendations
        
        recommendations = await recommendations.get_recommendations(user_id, num_films, num_genres)
        return recommendations
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))