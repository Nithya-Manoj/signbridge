from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class PredictionBase(BaseModel):
    predicted_sign: str
    confidence_score: float
    is_low_confidence: bool = False
    latency_ms: Optional[float] = None
    raw_landmark_summary: Optional[str] = None
    transcript_id: Optional[str] = None
    sign_class_id: Optional[str] = None


class PredictionCreate(PredictionBase):
    interview_id: str


class PredictionResponse(PredictionBase):
    id: str
    interview_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

