import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from backend.app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    # Role: 'candidate' | 'interviewer' | 'admin' (FR-01)
    role = Column(String(20), nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
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
    candidate_profile = relationship("Candidate", back_populates="user", uselist=False, cascade="all, delete-orphan")
    interviewer_profile = relationship("Interviewer", back_populates="user", uselist=False, cascade="all, delete-orphan")
    transcripts = relationship("Transcript", back_populates="speaker")

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"

