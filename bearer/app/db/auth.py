from .collections import auth_collection
from app.security_utils import verify_password

"""
You cannot create new authority from the api inteface!!!
"""


async def authenticate_authority(id: str, password: str) -> bool:
    result = await auth_collection.find_one({"username": id})
    if result is None:
        return False
    return verify_password(password, result["password"])
