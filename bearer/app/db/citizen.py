from typing import Optional
from app.models.citizen_model import CitizenModel
from .collections import citizen_collection

async def create_citizen(citizen_model:CitizenModel):
    citizen_collection.insert_one(citizen_model)

async def read_citizen(citizen_id:str) -> Optional[CitizenModel]:
    result = await citizen_collection.find_one({"PID" : citizen_id})
    if result is None:
        return None
    else:
        return CitizenModel(**result)

async def update_mail(citizen_id:str, mail:str) -> bool:
    result = citizen_collection.update_one({"PID" : citizen_id}, {"$set" : {"contact_mail" : mail}})
    return result.modified_count == 1

async def delete_citizen(citizen_id:str) -> bool:
    result = citizen_collection.delete_one({"PID" : citizen_id})
    return result.deleted_count == 1