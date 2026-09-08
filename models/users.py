from typing import List, Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="passenger")

    # Relationships
    rides_as_driver: Mapped[List["Ride"]] = relationship(
        "Ride",
        back_populates="driver",
        foreign_keys="Ride.driver_id"
    )
    vehicles: Mapped[List["Vehicle"]] = relationship(
        "Vehicle",
        back_populates="owner"
    )
