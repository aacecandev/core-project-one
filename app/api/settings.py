import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = bool(os.getenv("DEBUG", False))
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    DATABASE_URL: str
    DATABASE_NAME: str
    SENTRY_DSN: str
    MAX_CONNECTIONS_COUNT: int = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
    MIN_CONNECTIONS_COUNT: int = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))

    class Config:
        if os.path.exists(".env"):
            env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
