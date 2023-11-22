from aiohttp import ClientSession, TCPConnector
from loguru import logger


async def create_requests(url: str, params: dict) -> dict: 
    logger.info("Создаю запрос")
    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
        async with session.get(url=url, params=params) as response:
            logger.debug(f"response: {response}")
            logger.debug(f"response: {await response.text()}")
            return await response.json()

async def convert_cities_to_normal_type(cities: dict) -> dict:
    """
    Получает массив городов и преобразует в такой вид {name:id}
    """
    logger.debug(f"cities: {cities}")
    cities_dict = {}

    for item in cities["cities"]:
        logger.debug(f"item: {item}")
        cities_dict.setdefault(item["name"], item["id"])
    
    logger.debug(f"cities_dict: {cities_dict}")
    return cities_dict