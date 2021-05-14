from typing import List, Optional
from pydantic import BaseModel


class TokenData(BaseModel):
    username: Optional[str] = None
    scopes: List[str] = []


class Token(BaseModel):
    access_token: str
    token_type: str
