from urllib.parse import urljoin

import aiohttp
from fastapi import APIRouter
from loguru import logger

from ..config import *
from .logic import *


router =  APIRouter(
    prefix="/api_kinoafisha",
    tags=["Kinoafisha"]
)


@router.get("/get_all_cities/")
async def get_all_cities() -> dict:
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        url = "http://213.171.9.36/api_kinoafisha/get_all_cities/"

        async with session.get(url=url) as resp:
            logger.debug(f"response: {resp}")
            return {"msg" : "ok", "data" : await resp.json()}


@router.get("/get_schedule_events/")
async def get_schedule_events(city: str) -> dict:
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        url = "http://213.171.9.36/api_kinoafisha/get_schedule_events/"
        params = {"city": city}
        
        async with session.get(url=url, params=params) as response:
            logger.debug(f"response: {response}")
            logger.debug(f"response: {await response.json()}")
            return {"msg": "ok", "data": await response.json()}
