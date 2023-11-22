from datetime import datetime as dt, timedelta
from urllib.parse import urljoin

from aiohttp import ClientSession, TCPConnector
from loguru import logger

from .config import *


class GigaChatLogic:
    def __init__(self) -> None:
        self.basse_url = "https://gigachat.devices.sberbank.ru/api/v1/"
        self.access_token: str = None
        self.access_token_time: dt  = None

    async def __chek_valid_access_token(self):
        logger.debug(f"self.access_token: {self.access_token}")
        logger.debug(f"self.access_token_time: {self.access_token_time}")

        if self.access_token is None:
            await self.__get_access_token_and_time()
        if self.access_token_time is None:
            await self.__get_access_token_and_time()
        if self.access_token_time + timedelta(minutes=30) < dt.utcnow():
            await self.__get_access_token_and_time()

    async def __convert_unixtime_to_normal_view(self, time_unix: int) -> dt:
        """Переводит время из unix формата в %Y-%m-%d %H:%M:%S """
        time_unix /= 1000
        time = dt.utcfromtimestamp(time_unix).strftime('%Y-%m-%d %H:%M:%S')
        logger.debug(time)
        return dt.strptime(time, '%Y-%m-%d %H:%M:%S')

    async def __create_async_request(self, *, url: str, headers: dict, method:str, data:dict=None) -> dict:
        """Делает асинхронную сессию и запросы. Возвращает json"""
        logger.debug(f"url: {url} | headers: {headers} | method: {method} | data: {data}")
        try:
            match method:
                case "GET":
                    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
                        async with session.get(url=url, headers=headers) as response:
                            logger.debug(f"response: {response}")
                            logger.debug(f"response: {await response.json()}")
                            return await response.json()
                case "POST":
                    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
                        async with session.post(url=url, headers=headers, json=data) as response:
                            logger.debug(f"response: {response}")
                            logger.debug(f"response: {await response.json()}")
                            return await response.json()
                case _:
                    raise 
            
        except Exception as e:
            logger.opt(exception=e).critical("Error in __create_async_request")
            raise

    async def __get_access_token_and_time(self) -> None:  
        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            async with session.post(url=AUTH_URL, headers=AUTH_HEADERS, data=AUTH_DATA) as resp: 
                logger.debug(f"response_json: {await resp.json()}")
                response_json = await resp.json()

                self.access_token = response_json.get("access_token")
                unix_time = response_json.get("expires_at")
                self.access_token_time = await self.__convert_unixtime_to_normal_view(unix_time)
            
    async def get_gigachat_models(self) -> dict: 
        await self.__chek_valid_access_token()
        url = urljoin(self.basse_url, f"models")
        headers = {"Authorization" : f"Bearer {self.access_token}"}

        return await self.__create_async_request(url=url, headers=headers, method="GET")
            
    async def get_information_about_model(self, model: str) -> dict: 
        await self.__chek_valid_access_token()
        url = urljoin(self.basse_url, f"models/{model}")
        headers = {"Authorization" : f"Bearer {self.access_token}"}

        return await self.__create_async_request(url=url, headers=headers, method="GET")
    
    async def create_prompt(self, content: str) -> str:
        try:
            logger.debug(f"content: {content}")
            await self.__chek_valid_access_token()
            url = urljoin(self.basse_url, f"chat/completions")
            headers = {"Authorization" : f"Bearer {self.access_token}", "Content-Type": "application/json"}
            data = {
                "model": "GigaChat:latest", 
                "messages": [{
                    "role": "user", 
                    "content": f"\
                        Привет, посоветуй фильм на основе пожелания.\
                        Пожелание: {content}.", 
                }], 
                "temperature": 0.5,
                "max_tokens": 100}

            response = await self.__create_async_request(url=url, headers=headers, method="POST", data=data)
            return response["choices"][0]["message"]
        except Exception as e:
            logger.opt(exception=e).critical("Error im create promtr")
            raise

