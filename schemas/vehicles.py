from typing import Optional
import uuid
from pydantic import BaseModel, Field


class VehicleCreate(BaseModel):
    make: str = Field(..., min_length=1, max_length=100)
    model: str = Field(..., min_length=1, max_length=100)
    colour: str = Field(..., min_length=1, max_length=100)
    capacity: int = Field(..., ge=1, le=50)
    plate_number: str = Field(..., min_length=1, max_length=100)
    owner_id: Optional[uuid.UUID] = Field(default=None)
