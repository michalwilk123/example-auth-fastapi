from functools import lru_cache
from pydantic import BaseSettings
from pydantic.networks import EmailStr
from fastapi_mail import ConnectionConfig


@lru_cache
def get_db_settings():
    return DatabaseConfig()


@lru_cache
def get_mail_config():
    return EmailConfig()


SERVER_URL = "http://localhost:5000"


class DatabaseConfig(BaseSettings):
    MONGO_DB_USERNAME: str
    MONGO_DB_PASSWORD: str

    class Config:
        env_file = ".env"


class AppInformation(BaseSettings):
    APP_NAME: str = "Central Statistical Office"
    VERSION: str = "0.1"
    DESCRIPTION = "Bearer and citizen data distributor"


class SecurityConfig(BaseSettings):
    JWT_SECRET_KEY: str
    PASSWORD_PEPPER: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


class EmailConfig(BaseSettings):
    EMAIL_LOGIN: EmailStr
    EMAIL_PASSWORD: str
    EMAIL_UPDATE_EXPIRATION_PERIOD:int=5

    class Config:
        env_file = ".env"


# mail_connection_config = ConnectionConfig(
#     MAIL_USERNAME=get_mail_config().EMAIL_LOGIN,
#     MAIL_PASSWORD=get_mail_config().EMAIL_PASSWORD,

#     MAIL_PORT=587,
#     MAIL_SERVER="smtp.gmail.com",
#     MAIL_TLS=True,
#     MAIL_SSL=False,
# )

mail_connection_config = ConnectionConfig(
    MAIL_USERNAME = "Central Statistical Office App",
    MAIL_PASSWORD = get_mail_config().EMAIL_PASSWORD,
    MAIL_FROM = get_mail_config().EMAIL_LOGIN,
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Student debil",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True
)

MONGO_URL = (
    "mongodb+srv://"
    f"{get_db_settings().MONGO_DB_USERNAME}:"
    f"{get_db_settings().MONGO_DB_PASSWORD}"
    "@xavier-test.dbap4.mongodb.net"
    "/chat?retryWrites=true&w=majority"
)
