from fastapi.param_functions import Security
from app.security_utils import get_current_citizen, get_cred_exception
from app.models.citizen_model import (
    CitizenMailAuth,
    CitizenModel,
    CitizenDriveData,
    deprecate_to_driver_model,
)
from fastapi import APIRouter, HTTPException, status
from fastapi.security import HTTPBasic
from app.db import citizen
from typing import Union


citizen_router = APIRouter(prefix="/citizen")
security = HTTPBasic()


@citizen_router.get("")
async def read_citizen(
    citizen_pid: str, scope=Security(get_current_citizen, scopes=["all"])
) -> Union[None, CitizenModel, CitizenDriveData]:
    user = await citizen.read_citizen(citizen_pid)

    if user is None:
        raise get_cred_exception("")

    if scope == "all":
        return user
    elif scope == "driver_data":
        return deprecate_to_driver_model(user)


@citizen_router.post("")
async def create_citizen(
    citizen_model: CitizenModel,
    scope=Security(get_current_citizen, scopes=["all"])
):
    if scope == "all":
        success = await citizen.create_citizen(citizen_model)
        return {"success": success}
    else:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your access group has no permission to perform this operation")


@citizen_router.delete("")
async def delete_citizen(
    citizen_pid: str, scope=Security(get_current_citizen, scopes=["all"])
):
    if scope == "all":
        return citizen.delete_citizen(citizen_pid)
    else:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your access group has no permission to perform this operation")


@citizen_router.put("/mail")
async def update_mail(citizen_auth_model: CitizenMailAuth):
    # TODO: tutaj wysłany bedzie mail!!!
    ...
    # return citizen.update_mail(citizen_auth_model.PID, citizen_auth_model.name)


@citizen_router.get("/mail")
async def authorize_mail(token:str):
    ...
    # return citizen.update_mail(citizen_auth_model.PID, citizen_auth_model.name)