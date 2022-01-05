import asyncio

from bson import ObjectId, errors
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from settings import get_settings

settings = get_settings()

motor_client = AsyncIOMotorClient(
    settings.DATABASE_URL,
    maxPoolSize=settings.MAX_CONNECTIONS_COUNT,
    minPoolSize=settings.MIN_CONNECTIONS_COUNT,
)

motor_client.get_io_loop = asyncio.get_running_loop

database = motor_client[settings.DATABASE_NAME]


def get_database() -> AsyncIOMotorDatabase:
    return database


async def get_object_id(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except (errors.InvalidId, TypeError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
