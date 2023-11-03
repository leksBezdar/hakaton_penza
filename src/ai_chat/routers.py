from fastapi import APIRouter
from time import perf_counter

from .service import AIManager


router = APIRouter()


@router.post("/get_ai_avdvice")
def get_ai_advice(prompt: str):
    
    AIChat = AIManager()
    ai_chat = AIChat.ai_chat
    
    response = ai_chat.get_ai_advice(prompt=prompt)    
    
    return response