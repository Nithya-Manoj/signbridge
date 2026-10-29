import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Interviewer(Base):
    __tablename__ = "interviewers"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    department = Column(String(100), nullable=True)
    designation = Column(String(100), nullable=True)
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
    user = relationship("User", back_populates="interviewer_profile")
    interviews = relationship("Interview", back_populates="interviewer")
    questions = relationship("Question", back_populates="interviewer")

    def __repr__(self):
        return f"<Interviewer user_id={self.user_id} dept={self.department}>"

