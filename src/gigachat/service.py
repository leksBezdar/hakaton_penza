from datetime import datetime
from urllib.parse import urljoin

from aiohttp import ClientSession, TCPConnector
from loguru import logger

from .config import *


class GigaChatLogic:
    def __init__(self) -> None:
        self.basse_url = "https://gigachat.devices.sberbank.ru/api/v1/"
        self.access_token: str = None
        self.access_token_time = None

    async def chek_valid_access_token(self):
        if self.access_token is None:
            self._get_access_token_and_time()
        if self.access_token_time is None:
            ...

    async def convert_unixtime_to_normal_view(self, time_unix: int) -> datetime:
        time_unix /= 1000
        time = datetime.utcfromtimestamp(time_unix).strftime('%Y-%m-%d %H:%M:%S')
        logger.debug(time)
        return time

    async def _get_access_token_and_time(self) -> None:  
        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            async with session.post(url=AUTH_URL, headers=AUTH_HEADERS, data=AUTH_DATA) as resp: 
                logger.debug(f"response_json: {await resp.json()}")
                response_json = await resp.json()

                self.access_token = response_json.get("access_token")
                unix_time = response_json.get("expires_at")
                self.access_token_time = await self.convert_unixtime_to_normal_view(unix_time)
            
    async def _get_gigachat_models(self) -> dict: 
        await self.chek_valid_access_token()

        url = urljoin(self.basse_url, f"models")
        headers = {"Authorization" : f"Bearer {self.access_token}"}

        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            async with session.get(url=url, headers=headers) as response:
                logger.debug(f"response: {response}")
                return await response.json()
            
    async def _get_information_about_model(self, model: str) -> dict: 
        await  self.chek_valid_access_token()

        url = urljoin(self.basse_url, f"models/{model}")
        headers = {"Authorization" : f"Bearer {self.access_token}"}

        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            async with session.get(url=url, headers=headers) as response:
                logger.debug(f"response: {response}")
                return await response.json()