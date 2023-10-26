import requests

class IpDecoder:

    def _get_api_decoder_data(self, user_ip: str) -> dict:
        url = f"https://api.ipgeolocation.io/ipgeo?apiKey=2c687162d4e9429fb36decef1bd5ed27&ip={user_ip}&fields=city,latitude,longitude"
        response = requests.get(url).json()
        
        return response
    
    
    def get_user_location(self, user_ip: str):

        return self._get_api_decoder_data(user_ip)