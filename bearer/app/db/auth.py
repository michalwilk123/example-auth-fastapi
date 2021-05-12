from .collections import auth_collection

"""
You cannot create new authority from the api inteface!!!
Very very not secure!!
"""

async def authorize_authority(id:str, password:str) -> bool:
    result = await auth_collection.find_one({"cert_id": id, "password" : password})
    return result is not None
