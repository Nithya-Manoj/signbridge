import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Response(Base):
    __tablename__ = "responses"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    interview_question_id = Column(
        String(36), ForeignKey("interview_questions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    candidate_id = Column(
        String(36), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True
    )
    # Signs / landmark JSON metadata or notes recorded during the response
    raw_sign_data = Column(Text, nullable=True)
    # Translated or final text answer
    final_text_response = Column(Text, nullable=True)
    # Captioned speech if interviewer also spoke or clarified
    audio_caption_text = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    interview_question = relationship("InterviewQuestion", back_populates="responses")
    candidate = relationship("Candidate", back_populates="responses")

    def __repr__(self):
        return f"<Response candidate_id={self.candidate_id}>"
