from pydantic import BaseModel, Field

class VehicleCreate(BaseModel):
    make:str = Field(..., min_length=2, max_length=100)
    model:str = Field(..., min_length=2, max_length=100)             
    colour:str = Field(..., min_length=2, max_length=100)
    capacity:int = Field(...)
    plate_number:str = Field(..., min_length=2, max_length=100)