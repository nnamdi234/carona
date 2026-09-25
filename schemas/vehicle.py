import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class VehicleBase(BaseModel):
    make: str = Field(..., min_length=1, max_length=100, examples=["Toyota"])
    model: str = Field(..., min_length=1, max_length=100, examples=["Corolla"])
    colour: str = Field(..., min_length=1, max_length=100, examples=["Blue"])
    capacity: int = Field(..., ge=1, le=50, examples=[4])
    plate_number: str = Field(..., min_length=1, max_length=100, examples=["ABC-1234"])


class VehicleCreate(VehicleBase):
    owner_id: Optional[uuid.UUID] = Field(None, description="User ID of vehicle owner")


class VehicleUpdate(BaseModel):
    make: Optional[str] = Field(None, min_length=1, max_length=100)
    model: Optional[str] = Field(None, min_length=1, max_length=100)
    colour: Optional[str] = Field(None, min_length=1, max_length=100)
    capacity: Optional[int] = Field(None, ge=1, le=50)
    plate_number: Optional[str] = Field(None, min_length=1, max_length=100)
    owner_id: Optional[uuid.UUID] = None


class VehicleResponse(VehicleBase):
    id: uuid.UUID
    owner_id: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
