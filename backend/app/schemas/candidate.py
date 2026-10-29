from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from backend.app.schemas.user import UserResponse


class CandidateBase(BaseModel):
    phone: Optional[str] = None
    education: Optional[str] = None
    skills: Optional[str] = None
    resume_url: Optional[str] = None
    preferred_communication_mode: str = "isl"


class CandidateCreate(CandidateBase):
    user_id: str


class CandidateResponse(CandidateBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    user: Optional[UserResponse] = None

    model_config = ConfigDict(from_attributes=True)
