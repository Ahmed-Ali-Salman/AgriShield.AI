"""
Infrastructure ORM Model: AnomalyModel.
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, Float, String, Boolean, DateTime, JSON

from app.infrastructure.database.connection import Base


class AnomalyModel(Base):
    __tablename__ = "anomalies"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    supplier_id = Column(String(36), nullable=False, index=True)
    anomaly_type = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False, default=0.0)
    description = Column(String(2000), nullable=True)
    raw_data = Column(JSON, nullable=True)
    detected_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_confirmed = Column(Boolean, nullable=True)  # None = unreviewed
