import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, Text, DateTime
from backend.app.database import Base


class ModelVersion(Base):
    __tablename__ = "model_versions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    version_tag = Column(String(50), unique=True, index=True, nullable=False)
    # Model type: 'isolated_classifier' | 'transformer'
    model_type = Column(String(50), nullable=False)
    weights_path_or_url = Column(String(500), nullable=False)
    accuracy_metrics = Column(Text, nullable=True)  # JSON-encoded metrics e.g. {"accuracy": 0.94, "val_loss": 0.12}
    is_active = Column(Boolean, default=True, nullable=False)
    deployed_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self):
        return f"<ModelVersion {self.version_tag} ({self.model_type}) active={self.is_active}>"
