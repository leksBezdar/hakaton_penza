from fastapi import APIRouter

from .service import IpDecoder


router = APIRouter()


@router.get('/get_user_location')
async def get_user_location():
    
    user_location_decoder = IpDecoder()
    
    return user_location_decoder.get_user_location()