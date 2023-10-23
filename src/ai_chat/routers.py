from fastapi import APIRouter

from .service import AIChat


router = APIRouter()


@router.get("/get_ai_avdvice")
def get_ai_advice(prompt: str):
    
    response = AIChat.get_ai_advice(prompt=prompt)
    
    return response