from app.models.citizen_model import CitizenMailAuth
from app.models import CitizenModel
from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.db import citizen
from app.db.auth import authorize_authority
from typing import Optional


citizen_router = APIRouter(prefix='/citizen')
security = HTTPBasic()

@citizen_router.get('')
async def get_citizen(citizen_id:str, credentials:HTTPBasicCredentials=Depends(security)) -> Optional[CitizenModel]:
    if await authorize_authority(credentials.username, credentials.password):
        raise HTTPException(status_code=501, detail="not authorized")

    return await citizen.read_citizen(citizen_id)


@citizen_router.post('')
async def create_citizen(citizen_model:CitizenModel, credentials:HTTPBasicCredentials=Depends(security)): 
    if await authorize_authority(credentials.username, credentials.password):
        raise HTTPException(status_code=501, detail="not authorized")

    success = await citizen.create_citizen(citizen_model)
    return {"success" : success}


@citizen_router.delete('')
async def delete_citizen(citizen_id:str, credentials:HTTPBasicCredentials=Depends(security)):
    if await authorize_authority(credentials.username, credentials.password):
        raise HTTPException(status_code=501, detail="Bad credentials")

    return citizen.delete_citizen(citizen_id)


@citizen_router.put('/mail')
async def update_mail(citizen_auth_model:CitizenMailAuth):
    # TODO: tutaj wysłany bedzie mail!!!
    return citizen.update_mail(citizen_auth_model.PID, citizen_auth_model.name)

