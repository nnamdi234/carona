from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Float, DateTime
from models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey


class Ride(BaseModel):
    driver_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=True,
    )

    vehicle_id = mapped_column(
        UUID(as_uuid=True),                 
        ForeignKey("vehicle.id", ondelete="CASCADE"),
        nullable=True
    )

    route_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("route.id", ondelete="CASCADE"),
        nullable=True
    )

    origin = mapped_column(String(255), nullable=False)

    destination = mapped_column(String(255), nullable=False)

    distance_km = mapped_column(Float, nullable=False)   

    departure_time =  mapped_column(
        DateTime(timezone=True),
        nullable=True,   
    )      

    arrival_time = mapped_column(       
        DateTime(timezone=True),
        nullable=True,   
    )

    status = mapped_column(String(100), nullable=False, default="scheduled")

    fare = mapped_column(Float, nullable=False)
    