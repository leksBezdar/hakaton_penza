from fastapi import HTTPException


class InvalidListType(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid list type")


class FilmWasNotFound(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Film was not found")
