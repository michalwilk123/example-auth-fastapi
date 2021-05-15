from fastapi import Security
from pydantic.error_wrappers import ValidationError
from app.security_utils import get_current_citizen, get_cred_exception, security_config
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
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiosmtplib

citizen_router = APIRouter(prefix="/citizen")
security = HTTPBasic()
fast_mail = FastMail(mail_connection_config)


async def send_mail(payload:str, adresat, **params):
    MAIL_PARAMS = {'TLS': True, 'host': 'smtp.gmail.com', 'password': 'Wdctest4%', 'user': 'testwdc45@gmail.com', 'port': 587}
    mail_params = params.get("mail_params", MAIL_PARAMS)

    msg = MIMEMultipart()
    msg.preamble = "TEST"
    msg['Subject'] = "TEST3"
    msg['From'] = "testwdc45@gmail.com"
    adresat = adresat.split()
    msg['To'] = ', '.join(adresat)

    message = f"""
Subject: Test

{payload}
"""
    # msg.attach(MIMEText(message, "plain", 'utf-8'))
    msg.attach(MIMEText(message, "plain", 'utf-8'))

    host = mail_params.get('host', 'localhost')
    isSSL = mail_params.get('SSL', False);
    isTLS = mail_params.get('TLS', False);
    port = mail_params.get('port', 465 if isSSL else 25)
    smtp = aiosmtplib.SMTP(hostname=host, port=port, use_tls=isSSL)
    await smtp.connect()
    if isTLS:
        await smtp.starttls()
    if 'user' in mail_params:
        await smtp.login(mail_params['user'], mail_params['password'])
    await smtp.send_message(msg)
    await smtp.quit()

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
    scope=Security(get_current_citizen, scopes=["all"]),
):
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
    # normally creating the jwt token
    jwt_token = jwt.encode(
        EmailTokenPayload(
            data=citizen_auth_model, 
            expires=int(time.time()) + get_mail_config().EMAIL_UPDATE_EXPIRATION_PERIOD * 60
        ).dict(),
        security_config.JWT_SECRET_KEY,
        algorithm=security_config.ALGORITHM
    )

    template = f"""
<h2>Welcome to my app {citizen_auth_model.name}
{citizen_auth_model.surname}<h2/>
<b>Click below link to validate this email<b/>

<a href={SERVER_URL}/citizen/mail?token={jwt_token}>Click me<a/>

<i>If you did not requested mail update,
please ignore this mail.<i/>
"""
    await send_mail(template, citizen_auth_model.contact_mail)
    return {"success": True}


@citizen_router.get("/mail")
async def authorize_mail(token:str):
    try:
        payload = jwt.decode(
            token,
            security_config.JWT_SECRET_KEY,
            algorithms=[security_config.ALGORITHM]
        )
        citizen_data = payload.get("data")
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Cannot validate the update token for user"
        )
    
    success = await citizen.update_mail(citizen_data["PID"], citizen_data["contact_mail"])
    return {"success" : success}

