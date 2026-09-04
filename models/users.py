from sqlalchemy.orm import DeclarativeBase, mapped_column
import uuid 
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Integer  

class User(DeclarativeBase):
    id = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        nullable=False,
        default=uuid.uuid4
    )

    first_name = mapped_column(String(100), nullable=False) 

    Last_name = mapped_column(String(100), nullable=False)  

    email = mapped_column(String(100), nullable=False, unique=True)

    phone_number = mapped_column(String(100), nullable=True, unique=True)

    password = mapped_column(String(100), nullable=False)

    role = mapped_column(String(100), nullable=False)

