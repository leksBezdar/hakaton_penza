from loguru import logger


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