from sqlalchemy.orm import DeclarativeBase, mapped_column
import uuid     
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Integer, Float

class Route(DeclarativeBase):
    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        nullable=False,
        default=uuid.uuid4
    )

    origin = mapped_column(String(255), nullable=False)

    destination = mapped_column(String(255), nullable=False)

    distance_km = mapped_column(Float, nullable=False)

    estimated_duration_minutes = mapped_column(Float, nullable=False)