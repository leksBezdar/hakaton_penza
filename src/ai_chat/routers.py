from fastapi import APIRouter, Request, Response

from .service import AIManager


router = APIRouter()


@router.get("/get_ai_avdvice")
def get_ai_advice(prompt: dict):

    AIChat = AIManager()
    ai_chat = AIChat.ai_chat

    response = ai_chat.get_ai_advice(prompt=prompt)
    
    return response
