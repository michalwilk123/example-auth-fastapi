from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date
from fastapi import Query


class CitizenModel(BaseModel):
    """
    Model whitch defines the citizen, this will be
    actually stored in the mongodb database
    """

    name: str = Query(..., regex="[a-zA-Z]{3,40}")
    surname: str = Query(..., regex="[a-zA-Z]{3,40}")
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

    class Config:
        """
        This is an example for the citizen model
        """

        schema_extra = {
            "example": {
                "name": "john",
                "surname": "kowalski",
                "PID": "12345678911",
                "ID_card_number": "11111111111",
                "martial_status": "unknown",
                "driver_license_id": "0123456789A",
                "driver_license_exp_date": "2222-01-21",
                "driver_penalty_points": "10",
                "place_of_birth": "Warsaw",
                "residence": "Gdynia",
                "contact_number": "123456789",
                "contact_mail": "examplemail@mail.com",
            }
        }


class CitizenMailAuth(BaseModel):
    name: str = Query(..., regex="[a-zA-Z]{3,40}")
    surname: str = Query(..., regex="[a-zA-Z]{3,40}")
    PID: str = Query(..., regex="[0-9]{11}")
    contact_mail: Optional[EmailStr]

    class Config:
        schema_extra = {
            "example": {
                "name": "Tomasz",
                "surname": "Nowak",
                "PID": "12121223232",
                "contact_mail": "tomek@mail.pl",
            }
        }


class CitizenDriveData(BaseModel):
    name: str = Query(..., regex="[a-zA-Z]{3,40}")
    surname: str = Query(..., regex="[a-zA-Z]{3,40}")
    driver_license_id: Optional[str] = Query(None, regex="[A-Z0-9]{11}")
    driver_license_exp_date: Optional[date]
    driver_penalty_points: Optional[str] = Query(None, regex="[0-9]{0,3}")
    residence: str = Query(..., regex="[A-Za-z ]{2,100}")
    contact_number: Optional[str] = Query(..., regex="[0-9]{6,20}")
    contact_mail: Optional[EmailStr]

    class Config:
        schema_extra = {
            "example": {
                "name": "Karol",
                "surname": "Slowik",
                "driver_license_id": "0123456789A",
                "driver_license_exp_date": "2021-10-11",
                "driver_penalty_points": "0",
                "residence": "Gdansk",
                "contact_number": "420420420",
                "contact_mail": "slowik@wp.pl",
            }
        }


def deprecate_to_driver_model(citizen: CitizenModel) -> CitizenDriveData:
    return CitizenDriveData(
        name=citizen.name,
        surname=citizen.surname,
        driver_license_id=citizen.driver_license_id,
        driver_license_exp_date=citizen.driver_license_exp_date,
        driver_penalty_points=citizen.driver_penalty_points,
        residence=citizen.residence,
        contact_number=citizen.contact_number,
        contact_mail=citizen.contact_mail,
    )
