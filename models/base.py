from sqlalchemy.orm import DeclarativeBase, mapped_column
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import func, DateTime


class Base(DeclarativeBase):
    """Base class for all models."""



class BaseModel(Base):
    """Base model class with common attributes."""
    __abstract__ = True

    id = mapped_column(
            UUID(as_uuid=True),
            primary_key=True,
            index=True,
            nullable=False,
            default=uuid.uuid4
        )

    created_at = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),   
    )

    updated_at = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    deleted_at = mapped_column(
        DateTime(timezone=True),    
        nullable=True,
        default=None
    )
