from pydantic import BaseModel, Field

class VehicleCreate(BaseModel):
    make = Field(..., min_length=2, max_length=100)
    model = Field(..., min_length=2, max_length=100)             
    colour = Field(..., min_length=2, max_length=100)
    capacity = Field(..., min_length=2, max_length=100)
    plate_number = Field(..., min_length=2, max_length=100)