from .collections import auth_collection
from app.security_utils import verify_password
from typing import Tuple

"""
You cannot create new authority from the api inteface!!!
"""


async def authenticate_authority(id: str, password: str) -> Tuple[bool, str]:
    result = await auth_collection.find_one({"username": id})
    if result is None:
        return False, ""
    return verify_password(password, result["password"]), result["scope"]
