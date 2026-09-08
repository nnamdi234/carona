from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Integer
from models.base import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey


class Ride(BaseModel):


    driver_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=True,
        
    )