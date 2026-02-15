"""
Presentation: Pydantic Schemas — Supplier.

Request/response models for the API layer (validation + serialization).
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class SupplierCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    country: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., min_length=1, max_length=100)
    contact_email: str = Field(..., max_length=255)
    website: Optional[str] = Field(None, max_length=500)


class SupplierUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    country: Optional[str] = Field(None, min_length=1, max_length=100)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    contact_email: Optional[str] = Field(None, max_length=255)
    website: Optional[str] = Field(None, max_length=500)


class SupplierResponse(BaseModel):
    id: UUID
    name: str
    country: str
    category: str
    contact_email: str
    website: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
