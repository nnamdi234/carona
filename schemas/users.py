from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr = Field(...)
    phone_number: Optional[str] = Field(default=None, max_length=15)
    role: Optional[str] = Field(default="user")
    password: str = Field(..., min_length=6, max_length=100)

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    first_name: str
    last_name: str
    email: str
    phone_number: Optional[str] = None
    role: str
    created_at: datetime
    updated_at: datetime

class UserResponse(BaseModel):
    success: bool
    message: str
    data: UserOut

class UserListResponse(BaseModel):
    success: bool
    message: str
    data: list[UserOut]

class UserLogin(BaseModel):
    email: str = Field(...)
    password: str = Field(..., min_length=6, max_length=100)

class UserProfileUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    last_name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    phone_number: Optional[str] = Field(default=None, max_length=15)
