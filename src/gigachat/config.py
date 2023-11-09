import os 
from dotenv import load_dotenv


load_dotenv()

AUTH = os.environ.get("AUTH")
SCOPE = os.environ.get("SCOPE")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

AUTH_DATA = {"scope" : SCOPE}
AUTH_HEADERS = {
            "Authorization" : f"Bearer {AUTH}",
            "RqUID": CLIENT_ID,
            "Content-Type": "application/x-www-form-urlencoded"
            }
AUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"