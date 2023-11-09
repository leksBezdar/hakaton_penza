from typing import Literal
from pydantic import BaseModel


class ContentModel(BaseModel):
    role: Literal["user", "assistant"]
    content: str
