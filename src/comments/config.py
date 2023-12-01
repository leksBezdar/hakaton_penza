import os

from dotenv import load_dotenv

load_dotenv()


GUEST_NAME = os.environ.get('GUEST_NAME')
GUEST_ID = os.environ.get('GUEST_ID')
