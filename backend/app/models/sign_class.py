import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from backend.app.database import Base


class SignClass(Base):
    __tablename__ = "sign_classes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    label = Column(String(50), unique=True, index=True, nullable=False)
    display_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    # Category: 'greetings' | 'interview' | 'answers' | 'alphabet' | 'numbers'
    category = Column(String(50), default="interview", nullable=False)
    example_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    predictions = relationship("Prediction", back_populates="sign_class")

    def __repr__(self):
        return f"<SignClass {self.label} ({self.display_name})>"
