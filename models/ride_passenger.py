from sqlalchemy.orm import mapped_column
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from models.base import BaseModel


class RidePassenger(BaseModel):
    __tablename__ = "ride_passengers"

    ride_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("rides.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    passenger_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    status = mapped_column(
        String(50),
        nullable=False,
        default="booked"
    )
