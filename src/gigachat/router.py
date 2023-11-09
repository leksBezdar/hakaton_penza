from fastapi import APIRouter

from .service import GigaChatLogic


router = APIRouter(
    prefix="/gigachat",
    tags=["AI_Giga_Chat"]
)

@router.post("/get_access_token/")
async def token():
    gigachat = GigaChatLogic()
    return await gigachat._get_access_token_and_time()   

@router.get("/get_models/")
async def get_models():
    gigachat = GigaChatLogic()
    return await gigachat._get_gigachat_models()

@router.get("get_information_about_model")
async def get_information_about_model(model: str):
    gigachat = GigaChatLogic()
    return await  gigachat._get_information_about_model(model)
