from typing import List
from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import BaseModel


class Route(BaseModel):
    __tablename__ = "routes"

    origin: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    destination: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    distance_km: Mapped[float] = mapped_column(Float, nullable=False)
    estimated_duration_minutes: Mapped[float] = mapped_column(Float, nullable=False)

    # Relationships
    rides: Mapped[List["Ride"]] = relationship(
        "Ride",
        back_populates="route"
    )