from sqlalchemy.orm import DeclarativeBase, mapped_column
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Integer

class Ride(DeclarativeBase):
    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        nullable=False,
        default=uuid.uuid4
    )

    