from datetime import datetime
from typing import List, Optional

from models.base_model import MongoBaseModel
from pydantic import BaseModel, Field


class Location(BaseModel):
    coordinates: List[float] = Field(
        [2.125624418258667, 41.34004592895508], alias="coordinates"
    )
    type: str = Field("Point", alias="type")


class AccidentResponse(BaseModel):
    victims: int = Field(..., ge=0, lt=100, alias="victims")
    vehicles_involved: int = Field(..., ge=0, lt=100, alias="vehicles_involved")
    date: datetime = Field(..., alias="date")
    location: Location = Field(..., alias="location")


class AccidentRequest(AccidentResponse, MongoBaseModel):
    pass


class AccidentPostRequest(BaseModel):
    victims: int = Field(..., ge=0, lt=100, alias="victims")
    vehicles_involved: int = Field(..., ge=0, lt=100, alias="vehicles_involved")
    date: datetime
    location: Location = Field(..., alias="location")


class AccidentPostResponse(AccidentRequest, MongoBaseModel):
    pass


class AccidentPartialUpdateRequest(BaseModel):
    id: str = Field("ObjectId")
    victims: Optional[int] = Field(None, ge=0, lt=100, alias="victims")
    vehicles_involved: Optional[int] = Field(
        None, ge=0, lt=100, alias="vehicles_involved"
    )
    location: Optional[Location] = Field(None, alias="location")


class ResponseModel(BaseModel):
    message: str = Field(...)
