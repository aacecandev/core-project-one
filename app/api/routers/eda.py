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
    tags=["eda"],
    route_class=TimedRoute,
)


@router.get("/")
async def get_eda(
    database: AsyncIOMotorDatabase = Depends(get_database),
):
    return database["accidents"].find()


@router.get("/victims-grouped-month")
async def get_accidents_grouped_by_month(
    database: AsyncIOMotorDatabase = Depends(get_database),
):
    pipeline = [
        {"$project": {"_id": 0, "date": 1, "victims": 1}},
        {
            "$group": {
                "_id": {"month": {"$month": "$date"}},
                "average": {"$avg": "$victims"},
            },
        },
        {"$project": {"_id": 0, "month": "$_id.month", "average": 1}},
        {"$sort": {"month": 1}},
    ]
    return [accident async for accident in database["accidents"].aggregate(pipeline)]


@router.get("/victims-grouped-weekday")
async def get_accidents_grouped_by_weekday(
    database: AsyncIOMotorDatabase = Depends(get_database),
):
    pipeline = [
        {"$project": {"_id": 0, "date": 1, "victims": 1}},
        {
            "$group": {
                "_id": {"day": {"$dayOfWeek": "$date"}},
                "average": {"$avg": "$victims"},
            },
        },
        {"$project": {"_id": 0, "day": "$_id.day", "average": 1}},
        {"$sort": {"day": 1}},
    ]
    return [accident async for accident in database["accidents"].aggregate(pipeline)]


@router.get("/coordinates")
async def get_all_coordinates(
    database: AsyncIOMotorDatabase = Depends(get_database),
):
    pipeline = [
        {
            "$project": {
                "_id": 0,
                "long": {"$first": "$location.coordinates"},
                "lat": {"$last": "$location.coordinates"},
            }
        }
    ]
    return [accident async for accident in database["accidents"].aggregate(pipeline)]


@router.get("/vehicles-grouped-month")
async def get_vehicles_gruped_by_month(
    database: AsyncIOMotorDatabase = Depends(get_database),
):
    pipeline = [
        {"$project": {"_id": 0, "date": 1, "vehicles_involved": 1}},
        {
            "$group": {
                "_id": {"month": {"$month": "$date"}},
                "average": {"$avg": "$vehicles_involved"},
            },
        },
        {"$project": {"_id": 0, "month": "$_id.month", "average": 1}},
        {"$sort": {"month": 1}},
    ]
    return [accident async for accident in database["accidents"].aggregate(pipeline)]


@router.get("/vehicles-grouped-weekday")
async def get_vehicles_grouped_by_weekday(
    database: AsyncIOMotorDatabase = Depends(get_database),
):
    pipeline = [
        {"$project": {"_id": 0, "date": 1, "vehicles_involved": 1}},
        {
            "$group": {
                "_id": {"day": {"$dayOfWeek": "$date"}},
                "average": {"$avg": "$vehicles_involved"},
            },
        },
        {"$project": {"_id": 0, "day": "$_id.day", "average": 1}},
        {"$sort": {"day": 1}},
    ]
    return [accident async for accident in database["accidents"].aggregate(pipeline)]
