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
    async with aiohttp.ClientSession() as session:
        params = {"api_key": API_KEY}
        url = urljoin(BASE_URL, "cities")

        async with session.get(url=url, params=params) as resp:
            logger.debug(f"response: {resp}")
            cities = await resp.json()
            return {"msg" : "ok", "data" : await convert_cities_to_normal_type(cities)}


@router.get("/get_schedule_events/")
async def get_schedule_events(city: str,  date_end: datetime="") -> dict:
    async with aiohttp.ClientSession() as session:
        url = urljoin(BASE_URL, "schedule")
        params = {"api_key": API_KEY, "city": city, "date_end": date_end}
        
        async with session.get(url=url, params=params) as response:
            logger.debug(f"response: {response}")
            logger.debug(f"response: {response.text()}")
            return {"msg": "ok", "data": await response.json()}
