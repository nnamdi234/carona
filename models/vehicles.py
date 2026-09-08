from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer
from models.base import BaseModel

class Vehicle(BaseModel):
    make = mapped_column(String(100), nullable=False)

    model = mapped_column(String(100), nullable=False)

    colour = mapped_column(String(100),nullable=False)

    capacity = mapped_column(Integer, nullable=False)

    plate_number = mapped_column(String(100), nullable=False)

    