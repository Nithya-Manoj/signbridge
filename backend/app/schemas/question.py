from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class QuestionBase(BaseModel):
    question_text: str
    category: str = "general"
    difficulty: str = "medium"
    interviewer_id: Optional[str] = None


class QuestionCreate(QuestionBase):
    pass


class QuestionResponse(QuestionBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InterviewQuestionBase(BaseModel):
    question_order: int = 1
    custom_prompt: Optional[str] = None
    status: str = "pending"


class InterviewQuestionCreate(InterviewQuestionBase):
    interview_id: str
    question_id: Optional[str] = None


class InterviewQuestionResponse(InterviewQuestionBase):
    id: str
    interview_id: str
    question_id: Optional[str] = None
    created_at: datetime
    question: Optional[QuestionResponse] = None

    model_config = ConfigDict(from_attributes=True)
