from typing import List

from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from models.accidents import (
    AccidentPartialUpdateRequest,
    AccidentPostRequest,
    AccidentRequest,
    AccidentResponse,
    ResponseModel,
)
from motor.motor_asyncio import AsyncIOMotorDatabase
from routers.api_router import APIRouter, TimedRoute

from database.mongo import get_database, get_object_id

router = APIRouter(
    tags=["accidents_crud"],
    route_class=TimedRoute,
)


@router.get(
    "/",
    summary="Get a list of dictionaries for each accident",
    response_model=List[AccidentResponse],
    response_description="List of all accidents",
    responses={
        200: {"description": "The request was successful."},
        404: {"description": "The request doesn't return any data."},
    },
)
async def get_all_accidents(
    database: AsyncIOMotorDatabase = Depends(get_database),
) -> List[AccidentRequest]:
    """
    Get all accident documents

    The response model is an array of dictionaries with the following `key:value` structure:

    - victims: 0 >= integer <= 100
    - vehicles_involved: 0 >= integer <= 100
    - date: datetime
    - location:
        - coordinates: [float, float]
        - type: string

    It doesn't expect any query parameters either body.
    """
    try:
        accidents = [
            AccidentRequest(**accident)
            async for accident in database["accidents"].find()
        ]
        if accidents is None:
            JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "No accidents found"},
            )
            return None
        else:
            JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Successfully retrieved all accidents"},
            )
            return accidents
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )


@router.get(
    "/{id}",
    summary="Get a single dictionary for the specified accident",
    response_model=AccidentResponse,
    response_description="Get a single accident",
    responses={
        200: {"description": "The request was successful."},
        404: {"description": "The request doesn't return any data."},
        422: {"description": "The request is malformed."},
    },
)
async def get_accident(
    database: AsyncIOMotorDatabase = Depends(get_database),
    id: ObjectId = Depends(get_object_id),
) -> AccidentResponse:
    """
    Get a single accident document

    The response model is a dictionary with the following `key:value` structure:

    - victims: 0 >= integer <= 100
    - vehicles_involved: 0 >= integer <= 100
    - date: [Optional datetime] If not provided, a current timestamp will be used
    - location:
        - coordinates: [float, float]
        - type: string containing either "Point" or "LineString"

    It expects a single query parameter `id` which is a string containing a valid MongoDB ObjectId.
    """
    try:
        accident = await database["accidents"].find_one({"_id": id})
        if accident is None:
            JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "No accident found"},
            )
            return None
        else:
            JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"content": "Successfully retrieved accident"},
            )
            return accident
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )


@router.put(
    "/create",
    summary="Create a single accident",
    response_model=ResponseModel,
    response_description="Create a single accident",
    responses={
        200: {"description": "The request was successful."},
        422: {"description": "The request doesn't return any data."},
    },
)
async def create_post(
    payload: AccidentPostRequest,
    database: AsyncIOMotorDatabase = Depends(get_database),
) -> ResponseModel:
    """
    Create a single accident document

    The response model is a dictionary with the following `key:value` structure:

    - victims: 0 >= integer <= 100
    - vehicles_involved: 0 >= integer <= 100
    - date: [Optional datetime] If not provided, a current timestamp will be used
    - location:
        - coordinates: [float, float]
        - type: string containing either "Point" or "LineString"

    It expects a payload in the body containing a dictionary with the victims and the vehicles involved.
    """
    try:
        accident = payload.dict()
        inserted = await database["accidents"].insert_one(accident)
        if inserted.inserted_id is None:
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"message": "No accident found"},
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={"message": "Successfully created accident"},
            )
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )


@router.patch(
    "/update",
    summary="Update a single accident",
    response_model=ResponseModel,
    response_description="Update a single accident",
    responses={
        200: {"description": "The document was successfully updated"},
        422: {"description": "The document was not updated"},
    },
)
async def update(
    payload: AccidentPartialUpdateRequest,
    database: AsyncIOMotorDatabase = Depends(get_database),
) -> ResponseModel:
    """
    This endpoint updates a single document when being provided with a valid ObjectId string
    and the values to be updated within the payload.

    - victims: Optional[0 >= integer <= 100]
    - vehicles_involved: Optional[0 >= integer <= 100]
    - date: Optional[datetime]
    - location: [Optional]
        - coordinates: [float, float]
        - type: string containing either "Point" or "LineString"

    It returns a model that is a dictionary with the following `key:value` structure:

    - victims: 0 >= integer <= 100
    - vehicles_involved: 0 >= integer <= 100
    - date: datetime
    - location:
        - coordinates: [float, float]
        - type: string containing either "Point" or "LineString"
    """
    id = await get_object_id(payload.id)
    data = {
        "victims": payload.victims,
        "vehicles_involved": payload.vehicles_involved,
    }
    try:
        result = await database["accidents"].update_one({"_id": id}, {"$set": data})
        if result.modified_count != 0:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Successfully updated accident"},
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"message": "No accident found"},
            )
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )


@router.delete(
    "/delete/{id}",
    summary="Delete a single accident",
    response_model=ResponseModel,
    response_description="Delete a single accident",
    responses={
        200: {"description": "The request was successful."},
        422: {"description": "The request is malformed."},
    },
)
async def delete(
    database: AsyncIOMotorDatabase = Depends(get_database),
    id: ObjectId = Depends(get_object_id),
) -> ResponseModel:
    """
    This endpoint deletes a single document when being provided with a valid ObjectId string.
    within the payload.

    It expects the ObjectId to be passed as a string and returns a model that is a dictionary
    with the following `key:value` structure:

    - victims: 0 >= integer <= 100
    - vehicles_involved: 0 >= integer <= 100
    - date: datetime
    - location:
        - coordinates: [float, float]
        - type: string containing either "Point" or "LineString"
    """
    try:
        result = await database["accidents"].delete_one({"_id": id})
        print(dir(result))
        if result.deleted_count != 0:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Successfully deleted accident"},
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"message": "The accident has not been updated"},
            )
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(e)},
        )
