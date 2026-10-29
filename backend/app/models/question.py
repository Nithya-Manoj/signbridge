import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    interviewer_id = Column(String(36), ForeignKey("interviewers.id", ondelete="SET NULL"), nullable=True, index=True)
    question_text = Column(Text, nullable=False)
    # Category: 'technical' | 'behavioral' | 'introductory' | 'general'
    category = Column(String(50), default="general", nullable=False)
    # Difficulty: 'easy' | 'medium' | 'hard'
    difficulty = Column(String(20), default="medium", nullable=False)
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
    interviewer = relationship("Interviewer", back_populates="questions")
    interview_questions = relationship("InterviewQuestion", back_populates="question")

    def __repr__(self):
        return f"<Question {self.question_text[:30]}...>"


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    interview_id = Column(String(36), ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(String(36), ForeignKey("questions.id", ondelete="SET NULL"), nullable=True, index=True)
    question_order = Column(Integer, default=1, nullable=False)
    custom_prompt = Column(Text, nullable=True)
    # Status: 'pending' | 'active' | 'answered' | 'skipped'
    status = Column(String(20), default="pending", nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    interview = relationship("Interview", back_populates="interview_questions")
    question = relationship("Question", back_populates="interview_questions")
    responses = relationship("Response", back_populates="interview_question", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<InterviewQuestion order={self.question_order} status={self.status}>"

