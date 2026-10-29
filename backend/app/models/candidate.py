import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    education = Column(String(255), nullable=True)
    skills = Column(Text, nullable=True)
    resume_url = Column(String(500), nullable=True)
    # Preferred communication mode: 'isl', 'text', 'speech_caption', 'mixed'
    preferred_communication_mode = Column(String(50), default="isl", nullable=False)
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
    user = relationship("User", back_populates="candidate_profile")
    interviews = relationship("Interview", back_populates="candidate")
    responses = relationship("Response", back_populates="candidate")

    def __repr__(self):
        return f"<Candidate user_id={self.user_id}>"

