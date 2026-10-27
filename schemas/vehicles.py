from pydantic import BaseModel, Field
from typing import Optional

class VehicleCreate(BaseModel):
    make:str = Field(..., min_length=2, max_length=100)
    model:str = Field(..., min_length=2, max_length=100)             
    colour:str = Field(..., min_length=2, max_length=100)
    capacity:int = Field(...)
    plate_number:str = Field(..., min_length=2, max_length=100)


class VehicleUpdate(BaseModel):
    make:Optional[str] = Field(..., min_length=2, max_length=100)
    model: Optional[str] = Field(..., min_length=2, max_length=100)
    colour: Optional[str] = Field(..., min_length=2, max_length=100)
    capacity: Optional[str] = Field(...)
    plate_number: Optional[str] = Field(..., min_length=2, max_length=100)
