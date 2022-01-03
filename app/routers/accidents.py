from typing import List

from bson import ObjectId
from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from models.accidents import (AccidentPartialUpdateRequest,
                              AccidentPostRequest, AccidentPostResponse,
                              AccidentRequest, AccidentResponse)
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from routers.api_router import APIRouter
from settings import Settings

from database.mongo import get_database, get_object_id

# Great explanation on relative imports: https://fastapi.tiangolo.com/tutorial/bigger-applications/




settings = Settings()

router = APIRouter()


@router.get(
    "/",
    response_model=List[AccidentResponse],
    response_description="List of all accidents",
)
async def get_all_accidents(
    response: Response, database: AsyncIOMotorDatabase = Depends(get_database)
) -> List[AccidentRequest]:
    accidents = [
        AccidentRequest(**accident) async for accident in database["accidents"].find()
    ]
    if accidents is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No accidents found"
        )
    else:
        response.status_code = status.HTTP_200_OK
        return accidents


@router.get(
    "/{id}",
    response_model=AccidentResponse,
    status_code=status.HTTP_200_OK,
    response_description="Get a single accident",
)
async def get_accident(
    response: Response,
    database: AsyncIOMotorDatabase = Depends(get_database),
    id: ObjectId = Depends(get_object_id),
) -> AccidentResponse:
    accident = await database["accidents"].find_one({"_id": id})
    if accident is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        response.status_code = status.HTTP_200_OK
        return accident


@router.put(
    "/create",
    response_model=AccidentResponse,
    response_description="Create a single accident",
)
async def create_post(
    payload: AccidentPostRequest,
    response: Response,
    database: AsyncIOMotorDatabase = Depends(get_database),
) -> AccidentPostResponse:
    accident = payload.dict()
    inserted = await database["accidents"].insert_one(accident)
    result = await database["posts"].find_one({"_id": inserted.inserted_id})
    if result is not None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry was not created",
            headers={"X-Error": "Entry was not created"},
        )
    else:
        response.status_code = status.HTTP_201_CREATED
        return result


# curl -X PUT -H 'Content-type: application/json' --data '{"victims":"90", "vehicles_involved":"3"}' http://localhost:8000/accidents/create


@router.patch(
    "/update",
    # response_model=AccidentResponse
    status_code=status.HTTP_200_OK,
    response_description="Update a single accident",
)
async def update_post(
    payload: AccidentPartialUpdateRequest,
    database: AsyncIOMotorDatabase = Depends(get_database),
    responses={
        204: {"description": "The document was successfully updated"},
        400: {"description": "The document was not updated"},
    },
) -> AccidentResponse:
    id = await get_object_id(payload.id)
    data = payload.dict()
    del data["id"]
    result = await database["accidents"].update_one(
        {"_id": id}, {"$set": payload.dict(exclude_unset=True)}
    )
    if result.matched_count == 0:
        return JSONResponse(status_code=400)
        # raise HTTPException(
        #     detail="Entry was not updated",
        #     headers={"X-Error": "Entry was not updated"})
    else:
        print(dir(result))
        print(
            {
                "result": result.raw_result,
                "matched_count": result.matched_count,
                "modified_count": result.modified_count,
                "upserted_id": result.upserted_id,
                "acknowledged": result.acknowledged,
            }
        )
        return JSONResponse(
            status_code=204,
        )


@router.delete(
    "/delete/{id}",
    summary="Delete a single accident",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_post(
    database: AsyncIOMotorDatabase = Depends(get_database),
    id: ObjectId = Depends(get_object_id),
):
    print(id)
    result = await database["accidents"].delete_one({"_id": id})
    print(result)
    print(dir(result))
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry was not deleted",
            headers={"X-Error": "Entry was not deleted"},
        )
    else:
        return JSONResponse(
            status_code=204,
        )
