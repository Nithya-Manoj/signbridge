import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    interview_id = Column(String(36), ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False, index=True)
    transcript_id = Column(String(36), ForeignKey("transcripts.id", ondelete="SET NULL"), nullable=True, index=True)
    sign_class_id = Column(String(36), ForeignKey("sign_classes.id", ondelete="SET NULL"), nullable=True, index=True)
    predicted_sign = Column(String(100), nullable=False)
    # Confidence score (e.g. 0.95 -> 95%)
    confidence_score = Column(Float, nullable=False)
    # FR-10: every prediction carries a confidence score; low-confidence predictions are flagged
    is_low_confidence = Column(Boolean, default=False, nullable=False, index=True)
    # Translation latency in milliseconds to monitor sub-second requirement
    latency_ms = Column(Float, nullable=True)
    # Serialized landmark summary or bounding data
    raw_landmark_summary = Column(Text, nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    interview = relationship("Interview", back_populates="predictions")
    transcript = relationship("Transcript", back_populates="predictions")
    sign_class = relationship("SignClass", back_populates="predictions")

    def __repr__(self):
        return f"<Prediction {self.predicted_sign} conf={self.confidence_score:.2f} low_conf={self.is_low_confidence}>"

