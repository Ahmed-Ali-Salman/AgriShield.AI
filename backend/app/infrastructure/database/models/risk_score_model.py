"""
Infrastructure ORM Model: RiskScoreModel.

SQLAlchemy model for persisting Cyber-Food Risk Scores.
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, Float, String, DateTime, JSON

from app.infrastructure.database.connection import Base


class RiskScoreModel(Base):
    """SQLAlchemy ORM model for the risk_scores table."""

    __tablename__ = "risk_scores"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    supplier_id = Column(String(36), nullable=False, index=True)
    overall_score = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)
    signals = Column(JSON, nullable=True)  # Serialized ScoreSignals
    computed_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    notes = Column(String(1000), nullable=True)
