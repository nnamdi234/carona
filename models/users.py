from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    first_name = mapped_column(String(100), nullable=False) 
    last_name = mapped_column(String(100), nullable=False)  
    email = mapped_column(String(100), nullable=False, unique=True, index=True)
    phone_number = mapped_column(String(100), nullable=True, unique=True)
    password = mapped_column(String(255), nullable=False)
    role = mapped_column(String(50), nullable=False, default="passenger")

