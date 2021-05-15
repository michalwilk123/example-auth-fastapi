from pydantic import BaseModel


class Department(BaseModel):
    """
    Model of the department data
    stored in the database
    """
    name: str
    password: str
    scope: str
