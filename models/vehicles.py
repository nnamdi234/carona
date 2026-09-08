import uuid
from typing import List, Optional
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import BaseModel


class Vehicle(BaseModel):
    __tablename__ = "vehicles"

    owner_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    make: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    colour: Mapped[str] = mapped_column(String(100), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    plate_number: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)

    # Relationships
    owner: Mapped[Optional["User"]] = relationship(
        "User",
        back_populates="vehicles"
    )
    rides: Mapped[List["Ride"]] = relationship(
        "Ride",
        back_populates="vehicle"
    )