"""
Infrastructure ORM Model: SupplierModel.

SQLAlchemy model mapping for the Supplier domain entity.
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, Boolean, DateTime

from app.infrastructure.database.connection import Base


class SupplierModel(Base):
    """SQLAlchemy ORM model for the suppliers table."""

    __tablename__ = "suppliers"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, index=True)
    country = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    contact_email = Column(String(255), nullable=False)
    website = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
