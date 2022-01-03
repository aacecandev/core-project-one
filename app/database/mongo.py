from bson import ObjectId, errors
from fastapi import Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from settings import Settings

settings = Settings()

motor_client = AsyncIOMotorClient(
    settings.DATABASE_URL,
    maxPoolSize=settings.MAX_CONNECTIONS_COUNT,
    minPoolSize=settings.MIN_CONNECTIONS_COUNT,
)

database = motor_client[settings.DATABASE_NAME]


def get_database() -> AsyncIOMotorDatabase:
    return database


async def get_object_id(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except (errors.InvalidId, TypeError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


# async def get_document_or_404(
#     id: ObjectId = Depends(get_object_id),
#     database: AsyncIOMotorDatabase = Depends(get_database),
#     collection: str = "",
# ) -> AccidentBase:
#     document = await database[collection].find_one({"_id": id})
#     #raw_accidents = await database["accidents"].find_one({"_id": id})

#     if document is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

#     return **document
