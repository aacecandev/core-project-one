from datetime import datetime
from typing import List, Optional

from models.base_model import MongoBaseModel
from pydantic import BaseModel, Field


class Location(BaseModel):
    coordinates: List[float] = Field(..., alias="coordinates")
    type: str = Field(..., alias="type")


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
    date: datetime = Field(default_factory=datetime.now, alias="date")
    # location: Location = Field(..., alias="location")


class AccidentPostResponse(AccidentRequest, MongoBaseModel):
    pass


class AccidentPartialUpdateRequest(BaseModel):
    id: str = Field(...)
    victims: Optional[int] = Field(None, ge=0, lt=100, alias="victims")
    vehicles_involved: Optional[int] = Field(
        None, ge=0, lt=100, alias="vehicles_involved"
    )
