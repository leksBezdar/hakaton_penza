from urllib.parse import urljoin
from datetime import datetime

import aiohttp
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from loguru import logger

from ..config import *
from .logic import *


router =  APIRouter(
    prefix="/api_kinoafisha",
    tags=["Kinoafisha"]
)

@router.get("/get_all_cities/")
async def get_all_cities() -> dict:
    return RedirectResponse("http://213.171.9.36/api_kinoafisha/get_all_cities/")

@router.get("/get_schedule_events/")
async def get_schedule_events(city: str,  date_end: datetime="") -> dict:
    return RedirectResponse(f"http://213.171.9.36/api_kinoafisha/get_schedule_events/?city={city}&date_end={date_end}")