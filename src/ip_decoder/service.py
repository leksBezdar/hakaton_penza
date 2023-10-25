import requests


class IpDecoder:

    def _get_ip(self):
        response = requests.get('https://api64.ipify.org?format=json').json()
        return response["ip"]


    def _get_api_decoder_data(self) -> dict:
        ip_address = self._get_ip()
        url = f'http://ip-api.com/json/{ip_address}'
        response = requests.get(url).json()
        
        return response
    
    
    def get_user_location(self):
        
        response = self._get_api_decoder_data()
        
        location_data = {
            "city": response.get("city"),
            "latitude": response.get("lat"),
            "longitude": response.get("lon"),
        }
        return location_data