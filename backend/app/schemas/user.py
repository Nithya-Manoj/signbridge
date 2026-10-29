from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: str
    full_name: str
    role: Literal["candidate", "interviewer", "admin"]
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

