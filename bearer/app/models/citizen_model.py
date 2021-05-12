from typing import Optional
from pydantic import BaseModel


class CitizenModel(BaseModel):
    """
    Model whitch defines the citizen
    """
    name:str
    surname:str
    PID: str
    ID_card_number: str
    martial_status: Optional[str]
    driver_license_id: Optional[str]
    driver_license_exp_date: Optional[str]
    driver_penalty_points: Optional[str]
    place_of_birth: str
    residence: str
    contact_number: Optional[str]
    contact_mail: Optional[str]
