from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from backend.app.schemas.candidate import CandidateResponse
from backend.app.schemas.interviewer import InterviewerResponse
from backend.app.schemas.question import InterviewQuestionResponse


class InterviewBase(BaseModel):
    title: str
    scheduled_start: datetime
    duration_minutes: int = 45
    status: str = "scheduled"
    meeting_room_id: str
    notes: Optional[str] = None


class InterviewCreate(InterviewBase):
    candidate_id: str
    interviewer_id: str


class InterviewResponse(InterviewBase):
    id: str
    candidate_id: str
    interviewer_id: str
    created_at: datetime
    updated_at: datetime
    candidate: Optional[CandidateResponse] = None
    interviewer: Optional[InterviewerResponse] = None
    interview_questions: List[InterviewQuestionResponse] = []

    model_config = ConfigDict(from_attributes=True)
