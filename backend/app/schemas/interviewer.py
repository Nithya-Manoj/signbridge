from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from backend.app.schemas.user import UserResponse


class InterviewerBase(BaseModel):
    department: Optional[str] = None
    designation: Optional[str] = None


class InterviewerCreate(InterviewerBase):
    user_id: str


class InterviewerResponse(InterviewerBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    user: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)

