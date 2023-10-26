import requests
import socket
## getting the IP address using socket.gethostbyname() method
class IpDecoder:

    def _get_ip(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        print(ip_address)

        # response = requests.get('https://api64.ipify.org?format=json').json()
        return ip_address


    def _get_api_decoder_data(self) -> dict:
        ip_address = self._get_ip()
        url = f"https://api.ipgeolocation.io/ipgeo?apiKey=2c687162d4e9429fb36decef1bd5ed27&ip={ip_address}&fields=city,latitude,longitude"
        response = requests.get(url).json()
        
        return response
    
    
    def get_user_location(self):
        
        response = self._get_api_decoder_data()
        
        # location_data = {
        #     "city": response.get("city"),
        #     "latitude": response.get("lat"),
        #     "longitude": response.get("lon"),
        # }
        return response