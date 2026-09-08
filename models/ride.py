import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import BaseModel


class Ride(BaseModel):
    __tablename__ = "rides"

    driver_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    vehicle_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("vehicles.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    route_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("routes.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    origin: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    destination: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    departure_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    estimated_arrival_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    available_seats: Mapped[int] = mapped_column(Integer, nullable=False)
    total_seats: Mapped[int] = mapped_column(Integer, nullable=False)
    price_per_seat: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="SCHEDULED")
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relationships
    driver: Mapped["User"] = relationship(
        "User",
        back_populates="rides_as_driver",
        foreign_keys=[driver_id]
    )
    vehicle: Mapped[Optional["Vehicle"]] = relationship(
        "Vehicle",
        back_populates="rides",
        foreign_keys=[vehicle_id]
    )
    route: Mapped[Optional["Route"]] = relationship(
        "Route",
        back_populates="rides",
        foreign_keys=[route_id]
    )