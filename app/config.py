from functools import lru_cache
from pydantic import BaseSettings
from pydantic.networks import EmailStr


@lru_cache
def get_db_settings():
    return DatabaseConfig()


@lru_cache
def get_mail_config():
    return EmailConfig()


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

    class Config:
        env_file = ".env"


MONGO_URL = (
    "mongodb+srv://"
    f"{get_db_settings().MONGO_DB_USERNAME}:"
    f"{get_db_settings().MONGO_DB_PASSWORD}"
    "@xavier-test.dbap4.mongodb.net"
    "/chat?retryWrites=true&w=majority"
)
