import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    candidate_id = Column(String(36), ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False, index=True)
    interviewer_id = Column(String(36), ForeignKey("interviewers.id", ondelete="CASCADE"), nullable=False, index=True)
    scheduled_start = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, default=45, nullable=False)
    # Status: 'scheduled' | 'in_progress' | 'completed' | 'cancelled'
    status = Column(String(30), default="scheduled", nullable=False, index=True)
    meeting_room_id = Column(String(64), unique=True, nullable=False, index=True)
    notes = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    candidate = relationship("Candidate", back_populates="interviews")
    interviewer = relationship("Interviewer", back_populates="interviews")
    interview_questions = relationship(
        "InterviewQuestion",
        back_populates="interview",
        cascade="all, delete-orphan",
        order_by="InterviewQuestion.question_order",
    )
    transcripts = relationship(
        "Transcript",
        back_populates="interview",
        cascade="all, delete-orphan",
        order_by="Transcript.timestamp",
    )
    predictions = relationship(
        "Prediction",
        back_populates="interview",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Interview {self.title} status={self.status}>"

