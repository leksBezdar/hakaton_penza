from fastapi import APIRouter

from .service import GigaChatLogic


router = APIRouter(
    prefix="/gigachat",
    tags=["AI_Giga_Chat"]
)


@router.get("/get_models/")
async def get_models():
    gigachat = GigaChatLogic()
    return await gigachat.get_gigachat_models()

@router.get("get_information_about_model/")
async def get_information_about_model(model: str):
    gigachat = GigaChatLogic()
    return await  gigachat.get_information_about_model(model)

@router.post("/create_prompt/")
async def create_promtp(content: str): 
    gigachat = GigaChatLogic()
    return await gigachat.create_prompt(content)