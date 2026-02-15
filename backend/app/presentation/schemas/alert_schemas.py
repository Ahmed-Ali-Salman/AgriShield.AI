"""Pydantic Schemas: Alert."""
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class AlertCreateRequest(BaseModel):
    supplier_id: UUID
    title: str = Field(..., max_length=255)
    description: str = Field("", max_length=2000)
    severity: str = Field("info")

class AlertResponse(BaseModel):
    id: UUID
    supplier_id: UUID
    title: str
    description: str
    severity: str
    status: str
    triggered_at: datetime
    resolved_at: Optional[datetime]
    class Config:
        from_attributes = True
