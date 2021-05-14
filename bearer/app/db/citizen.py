from typing import Optional
from app.models.citizen_model import CitizenModel
from .collections import citizen_collection
import json


async def create_citizen(citizen_model: CitizenModel) -> bool:
    doc = await citizen_collection.find_one({"PID": citizen_model.PID})
    if doc is not None:
        return False

    # i know that is bad but i dont know how to solve it
    cit_json = json.loads(citizen_model.json()) 
    await citizen_collection.insert_one(cit_json)
    return True


async def read_citizen(citizen_id: str) -> Optional[CitizenModel]:
    result = await citizen_collection.find_one({"PID": citizen_id})
    if result is None:
        return None
    else:
        return CitizenModel(**result)


async def update_mail(citizen_id: str, mail: str) -> bool:
    result = citizen_collection.update_one(
        {"PID": citizen_id}, {"$set": {"contact_mail": mail}}
    )
    return result.modified_count == 1


async def delete_citizen(citizen_id: str) -> bool:
    result = citizen_collection.delete_one({"PID": citizen_id})
    return result.deleted_count == 1
