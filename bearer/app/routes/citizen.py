from app.models.citizen_model import CitizenModel
from fastapi import APIRouter, Depends, Body
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app import db
from typing import Optional


citizen_router = APIRouter(prefix='/citizen')
security = HTTPBasic()

@citizen_router.get('')
async def get_citizen(citizen_id:str, credentials:HTTPBasicCredentials=Depends(security)) -> Optional[CitizenModel]:
    return await db.citizen.read_citizen(citizen_id)


@citizen_router.post('')
async def create_citizen(citizen_model:CitizenModel, credentials:HTTPBasicCredentials=Depends(security)): 
    success = await db.citizen.create_citizen(citizen_model)
    return {"successful" : success}


@citizen_router.delete('')
async def delete_citizen(citizen_id:str, credentials:HTTPBasicCredentials=Depends(security)):
    return db.citizen.delete_citizen(citizen_id)


@citizen_router.put('/mail')
async def update_mail(citizen_id:str, credentials:HTTPBasicCredentials=Depends(security), mail:str=Body(...)):
    return db.citizen.update_mail(citizen_id, mail)

