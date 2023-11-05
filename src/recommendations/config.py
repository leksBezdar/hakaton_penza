import os

from dotenv import load_dotenv

load_dotenv()

SIMILARITY_COEFFICIENT = os.environ.get("SIMILARITY_COEFFICIENT")
THRESHOLD_FOR_POSITIVE_RATING = os.environ.get("THRESHOLD_FOR_POSITIVE_RATING")
