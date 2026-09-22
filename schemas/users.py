from typing import Optional
from pydantic import Field, EmailStr


class UserCreate:
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr = Field(...)
    phone_number: Optional[str] = Field(..., max_length=15)
    role: str = Field(...)
    password: str = Field(..., min_length = 6, max_length=100)


class UserLogin:
    email: str = Field(...)
    password: str = Field(..., min_length = 6, max_length=100)