from fastapi import Security
from pydantic.error_wrappers import ValidationError
from app.security_utils import (
    get_current_citizen,
    get_cred_exception,
    security_config,
)
from app.models.citizen_model import (
    CitizenMailAuth,
    CitizenModel,
    CitizenDriveData,
    deprecate_to_driver_model,
)
from fastapi import APIRouter, HTTPException, status
from fastapi_mail import FastMail, MessageSchema
from fastapi.security import HTTPBasic
from app.db import citizen
from typing import Union
from app.config import get_mail_config, mail_connection_config, SERVER_URL
from app.models.token_models import EmailTokenPayload
from jose import jwt, JWTError
import time

citizen_router = APIRouter(prefix="/citizen")
security = HTTPBasic()
fast_mail = FastMail(mail_connection_config)


@citizen_router.get("")
async def read_citizen(
    citizen_pid: str, scope=Security(get_current_citizen, scopes=["all"])
) -> Union[None, CitizenModel, CitizenDriveData]:
    """
    Read citizen related data. Needs authorization
    from the client
    """
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
    scope=Security(get_current_citizen, scopes=["all"]),
):
    """
    Assign new citizen to the database.
    Need special permissions to perform the operation
    """
    if scope == "all":
        success = await citizen.create_citizen(citizen_model)
        return {"success": success}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your access group has no permission to "
            "perform this operation",
        )


@citizen_router.delete("")
async def delete_citizen(
    citizen_pid: str, scope=Security(get_current_citizen, scopes=["all"])
):
    """
    Delete user with given PID number.
    Needs elevated permissions.
    Returns 401 error when not authorized
    """
    if scope == "all":
        return citizen.delete_citizen(citizen_pid)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your access group has no permission to perform"
            " this operation",
        )


@citizen_router.put("/mail")
async def update_mail(citizen_auth_model: CitizenMailAuth):
    """
    Propose new mail to update for the api. Proposed
    mail needs to be validated, so as the result,
    application sends a mail message with a link with
    atached jwt token
    """
    jwt_token = jwt.encode(
        EmailTokenPayload(
            data=citizen_auth_model,
            expires=int(time.time())
            + get_mail_config().EMAIL_UPDATE_EXPIRATION_PERIOD * 60,
        ).dict(),
        security_config.JWT_SECRET_KEY,
        algorithm=security_config.ALGORITHM,
    )

    template = f"""
<h2>Welcome to my app {citizen_auth_model.name}
{citizen_auth_model.surname}<h2/>
<b>Click below link to validate this email<b/>

<a href={SERVER_URL}/citizen/mail?token={jwt_token}>Click me<a/>

<i>If you did not requested mail update,
please ignore this mail.<i/>
"""

    message = MessageSchema(
        subject="Update your mail",
        recipients=[citizen_auth_model.contact_mail],
        body=template,
        subtype="html",
    )

    await fast_mail.send_message(message)
    return {"success": True}


@citizen_router.get("/mail")
async def authorize_mail(token: str):
    """
    You will probably access this link
    from your email.
    Validate app generated token JWT
    token to authorize your mail
    address
    """
    response = {}
    try:
        payload = jwt.decode(
            token,
            security_config.JWT_SECRET_KEY,
            algorithms=[security_config.ALGORITHM],
        )
        response["payload-validated"] = True

        citizen_data = payload.get("data")
        response["payload"] = citizen_data
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cannot validate the update token for user",
        )

    success = await citizen.update_mail(
        citizen_data["PID"], citizen_data["contact_mail"]
    )
    response["mail-update-status"] = success
    return response
