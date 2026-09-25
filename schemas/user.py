import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100, examples=["John"])
    last_name: str = Field(..., min_length=1, max_length=100, examples=["Doe"])
    email: EmailStr = Field(..., examples=["john.doe@example.com"])
    phone_number: Optional[str] = Field(None, max_length=100, examples=["+1234567890"])
    role: str = Field("passenger", max_length=50, examples=["passenger"])


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100, examples=["securepassword123"])


class UserLogin(BaseModel):
    email: EmailStr = Field(..., examples=["john.doe@example.com"])
    password: str = Field(..., examples=["securepassword123"])


class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
