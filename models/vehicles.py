from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer
from models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey

class Vehicle(BaseModel):
    __tablename__ = "vehicles"

    make = mapped_column(String(100), nullable=False)
    model = mapped_column(String(100), nullable=False)
    colour = mapped_column(String(100), nullable=False)
    capacity = mapped_column(Integer, nullable=False)
    plate_number = mapped_column(String(100), nullable=False, unique=True)
    owner_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
    )