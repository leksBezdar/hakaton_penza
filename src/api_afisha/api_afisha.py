from urllib.parse import urljoin
from datetime import datetime

import aiohttp
from fastapi import APIRouter
from loguru import logger

from ..config import *
from .utils import *


router =  APIRouter(
    prefix="/api_kinoafisha",
    tags=["Kinoafisha"]
)

@router.get("/get_all_cities/")
async def get_all_cities() -> dict:
    url = urljoin(BASE_URL, "cities")
    params = {"api_key": API_KEY}
    cities = await create_requests(url, params)
    return {"msg" : "ok", "data" : await convert_cities_to_normal_type(cities)}


@router.get("/get_schedule_events/")
async def get_schedule_events(city: str,  date_end: datetime="") -> dict:
    url = urljoin(BASE_URL, "schedule")
    params = {"api_key": API_KEY, "city": city, "date_end": date_end}
    events = await create_requests(url, params)
    return {"msg": "ok", "data": events}
