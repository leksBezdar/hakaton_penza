from datetime import datetime as dt, timedelta
from urllib.parse import urljoin

from aiohttp import ClientSession, TCPConnector
from loguru import logger

from .scheme import ContentModel
from .config import *


class GigaChatLogic:
    def __init__(self) -> None:
        self.basse_url = "https://gigachat.devices.sberbank.ru/api/v1/"
        self.access_token: str = None
        self.access_token_time = None

    async def chek_valid_access_token(self):
        logger.debug(f"self.access_token: {self.access_token}")
        logger.debug(f"self.access_token_time: {self.access_token_time}")

        if self.access_token is None:
            await self._get_access_token_and_time()
        if self.access_token_time is None:
            await self._get_access_token_and_time()

    async def convert_unixtime_to_normal_view(self, time_unix: int) -> dt:
        time_unix /= 1000
        time = dt.utcfromtimestamp(time_unix).strftime('%Y-%m-%d %H:%M:%S')
        logger.debug(time)
        return time

    async def _get_access_token_and_time(self) -> None:  
        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            async with session.post(url=AUTH_URL, headers=AUTH_HEADERS, data=AUTH_DATA) as resp: 
                logger.debug(f"response_json: {await resp.json()}")
                response_json = await resp.json()

                self.access_token = response_json.get("access_token")
                logger.debug(self.access_token)
                unix_time = response_json.get("expires_at")
                self.access_token_time = await self.convert_unixtime_to_normal_view(unix_time)
            
    async def _get_gigachat_models(self) -> dict: 
        await self.chek_valid_access_token()
        logger.debug(self.access_token)
        url = urljoin(self.basse_url, f"models")
        headers = {"Authorization" : f"Bearer {self.access_token}"}

        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            async with session.get(url=url, headers=headers) as response:
                logger.debug(f"response: {response}")
                return await response.json()
            
    async def _get_information_about_model(self, model: str) -> dict: 
        await self.chek_valid_access_token()

        url = urljoin(self.basse_url, f"models/{model}")
        headers = {"Authorization" : f"Bearer {self.access_token}"}

        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            async with session.get(url=url, headers=headers) as response:
                logger.debug(f"response: {response}")
                return await response.json()
    
    async def _create_prompt(self, content: str) -> str:
        await self.chek_valid_access_token()
        logger.debug(f"content: {content}")
        url = urljoin(self.basse_url, f"chat/completions")
        headers = {"Authorization" : f"Bearer {self.access_token}", "Content-Type": "application/json"}
        data = {
            "model": "GigaChat:latest", 
            "messages": [{
                "role": "user", 
                "content": f"\
                    Привет, посоветуй фильм пользователю на основе его желания.\
                    Желание пользователя: {content}.\
                    А также можешь представить, будто ты общаешься с пользователем и отвечаешь ему.", 
            }], 
            "temperature": 0.5,
            "max_tokens": 100}

        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            async with session.post(url=url, headers=headers, json=data) as response:
                logger.debug(f"response: {response}")
                logger.debug(f"response: {await response.json()}")
                response_json = await response.json()
                response_from_ai = response_json["choices"][0]["message"]
                return response_from_ai