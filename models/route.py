from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Float
from models.base import BaseModel

class Route(BaseModel):

    origin = mapped_column(String(255), nullable=False)

    destination = mapped_column(String(255), nullable=False)

    distance_km = mapped_column(Float, nullable=False)

    estimated_duration_minutes = mapped_column(Float, nullable=False)