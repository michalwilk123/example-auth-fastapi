from functools import lru_cache
from pydantic import BaseSettings


@lru_cache
def get_db_settings():
    return Settings()


class Settings(BaseSettings):
    xavier_mongo_db_username: str
    xavier_mongo_db_password: str

    class Config:
        env_file = ".env"


class AppInformation(BaseSettings):
    APP_NAME: str = "Central Statistical Office"
    VERSION: str = "0.1"
    DESCRIPTION = "Bearer and citizen data distributor"


MONGO_URL = (
    "mongodb+srv://"
    f"{get_db_settings().xavier_mongo_db_username}:"
    f"{get_db_settings().xavier_mongo_db_password}"
    "@xavier-test.dbap4.mongodb.net"
    "/chat?retryWrites=true&w=majority"
)
