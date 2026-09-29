from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr = Field(...)
    phone_number: Optional[str] = Field(default=None, max_length=15)
    role: Optional[str] = Field(default="user")
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    email: str = Field(...)
    password: str = Field(..., min_length=6, max_length=100)