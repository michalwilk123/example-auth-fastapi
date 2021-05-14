from os import stat
from fastapi import Depends, status, Security
from passlib.context import CryptContext
from datetime import timedelta, datetime
from typing import Optional, Union
from app.config import SecurityConfig
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from fastapi import HTTPException
from pydantic import ValidationError
from app.models.token_models import TokenData
from app.db.citizen import read_citizen
from app.models.citizen_model import (
    CitizenDriveData,
    CitizenModel,
    deprecate_to_driver_model,
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security_config = SecurityConfig()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "all": "All informations about the citizen",
        "driving_data": "Informations related with driving",
    },
)


def get_password_hash(plain_password: str):
    return pwd_context.hash(plain_password + security_config.PASSWORD_PEPPER)


def verify_password(plain_password: str, hashed) -> bool:
    return pwd_context.verify(
        plain_password + security_config.PASSWORD_PEPPER, hashed
    )


def create_access_token(data: dict, expires_time: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_time:
        expire = datetime.utcnow() + expires_time
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=security_config.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(
        to_encode,
        security_config.JWT_SECRET_KEY,
        algorithm=security_config.ALGORITHM,
    )
    return encoded_jwt


def get_cred_exception(
    value: str, detail: str = "Could not validate credentials"
):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": value},
    )


async def get_current_citizen(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
) -> str:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"

    cred_exception = get_cred_exception(authenticate_value)

    try:
        payload = jwt.decode(
            token,
            security_config.JWT_SECRET_KEY,
            algorithms=[security_config.ALGORITHM],
        )
        username = payload.get("sub")
        if username is None:
            raise cred_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise cred_exception

    assert token_data.username is not None

    if len(token_data.scopes) != 1:
        raise get_cred_exception(
            authenticate_value,
            "You cannot set more than one scope in this app",
        )

    return token_data.scopes[0]
