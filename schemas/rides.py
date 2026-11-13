from pydantic import AwareDatetime, BaseModel, Field
from uuid import UUID


class RideCreate(BaseModel):
    vehicle_id:UUID
    origin: str = Field(..., min_length=255)
    destination:str = Field(..., min_length=2, max_length=255)
    departure_time: AwareDaretime
    seats_offered: int = fIELD(..., ge=1)
    fare: float = Field(..., gt 0)