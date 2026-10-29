from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class TranscriptBase(BaseModel):
    speaker_role: str
    message_type: str
    content: str
    confidence_score: Optional[float] = None
    speaker_id: Optional[str] = None


class TranscriptCreate(TranscriptBase):
    interview_id: str


class TranscriptResponse(TranscriptBase):
    id: str
    interview_id: str
    timestamp: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
