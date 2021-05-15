from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security import (
    OAuth2PasswordRequestForm,
)
from app.models.token_models import Token
from app.db.auth import authenticate_authority
from datetime import timedelta
from app.security_utils import security_config, create_access_token

security_router = APIRouter()


@security_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    Log in to your account using oauth2 authorization.
    In response we get an jwt authorization token
    which is used for granting access to data
    """
    is_auth, scope = await authenticate_authority(
        form_data.username, form_data.password
    )

    if not is_auth:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token_expires = timedelta(
        minutes=security_config.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data={"sub": form_data.username, "scopes": [scope]},
        expires_time=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}
