"""
Infrastructure ORM Model: AlertModel.
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime

from app.infrastructure.database.connection import Base


class AlertModel(Base):
    __tablename__ = "alerts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    supplier_id = Column(String(36), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(2000), nullable=True)
    severity = Column(String(20), nullable=False, default="info")
    status = Column(String(20), nullable=False, default="open", index=True)
    triggered_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    resolved_at = Column(DateTime, nullable=True)
