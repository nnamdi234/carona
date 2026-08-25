from sqlalchemy.orm import DeclarativeBase, mapped_column
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Integer

class Vehicle(DeclarativeBase):
    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        nullable=False,
        default=uuid.uuid4
    )

    make = mapped_column(String(100), nullable=False)

    model = mapped_column(String(100), nullable=False)

    colour = mapped_column(String(100),nullable=False)

    capacity = mapped_column(String(100), nullable=False)

    plate_number = mapped_column(String(100), nullable=False)