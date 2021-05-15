from app.models.citizen_model import CitizenMailAuth
from typing import List, Optional
from pydantic import BaseModel


class TokenData(BaseModel):
    """
    Payload of the simple oauth2 token
    """

    username: Optional[str] = None
    scopes: List[str] = []


class Token(BaseModel):
    """
    Simple token model
    """

    access_token: str
    token_type: str


class EmailTokenPayload(BaseModel):
    """
    Payload of the jwt token needed for
    validating the mail.
    """

    data: CitizenMailAuth
    expires: int
