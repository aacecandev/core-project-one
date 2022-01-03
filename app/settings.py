import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    ENVIRONMENT: str
    DATABASE_URL: str
    DATABASE_NAME: str
    MAX_CONNECTIONS_COUNT: int = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
    MIN_CONNECTIONS_COUNT: int = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))

    class Config:
        if os.path.exists(".env"):
            env_file = ".env"
