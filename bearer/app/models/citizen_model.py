from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date
from fastapi import Query


class CitizenModel(BaseModel):
    """
    Model whitch defines the citizen, this will be
    actually stored in the mongodb database
    """
    name:str = Query(..., regex="[a-zA-Z]{3,40}")
    surname:str = Query(..., regex="[a-zA-Z]{3,40}")
    PID: str = Query(..., regex="[0-9]{11}")
    ID_card_number: str = Query(..., regex="[A-Z0-9]{11}")
    martial_status: Optional[str] = Query(None, max_length=50)
    driver_license_id: Optional[str] = Query(None, regex="[A-Z0-9]{11}")
    driver_license_exp_date: Optional[date]
    driver_penalty_points: Optional[str] = Query(None, regex="[0-9]{0,3}")
    place_of_birth: str = Query(..., regex="[A-Za-z ]{2,100}")
    residence: str = Query(..., regex="[A-Za-z ]{2,100}")
    contact_number: Optional[str] = Query(..., regex="[0-9]{6,20}")
    contact_mail: Optional[EmailStr]


class CitizenMailAuth(BaseModel):
    name:str = Query(..., regex="[a-zA-Z]{3,40}")
    surname:str = Query(..., regex="[a-zA-Z]{3,40}")
    PID: str = Query(..., regex="[0-9]{11}")
    contact_mail: Optional[EmailStr]