import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Transcript(Base):
    __tablename__ = "transcripts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    interview_id = Column(String(36), ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False, index=True)
    # Speaker role: 'interviewer' | 'candidate' | 'system'
    speaker_role = Column(String(20), nullable=False)
    # Speaker ID (nullable for system messages)
    speaker_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    # Message type: 'speech_caption' (STT) | 'sign_prediction' (ISL translation) | 'system'
    message_type = Column(String(30), nullable=False, index=True)
    # The actual spoken / translated text content
    content = Column(Text, nullable=False)
    # Timestamped log of both sides
    timestamp = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
    # Optional overall confidence score if applicable
    confidence_score = Column(Float, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    interview = relationship("Interview", back_populates="transcripts")
    speaker = relationship("User", back_populates="transcripts")
    predictions = relationship("Prediction", back_populates="transcript")

    def __repr__(self):
        return f"<Transcript role={self.speaker_role} type={self.message_type} text={self.content[:25]}>"

