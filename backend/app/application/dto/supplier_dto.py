"""
Application DTO: Supplier Data Transfer Objects.

DTOs used to cross layer boundaries without exposing domain internals.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from app.domain.entities.supplier import Supplier


@dataclass
class CreateSupplierDTO:
    """Input DTO for creating a supplier."""
    name: str
    country: str
    category: str
    contact_email: str
    website: Optional[str] = None


@dataclass
class UpdateSupplierDTO:
    """Input DTO for updating a supplier (all fields optional)."""
    name: Optional[str] = None
    country: Optional[str] = None
    category: Optional[str] = None
    contact_email: Optional[str] = None
    website: Optional[str] = None


@dataclass
class SupplierResponseDTO:
    """Output DTO returned from use cases."""
    id: UUID
    name: str
    country: str
    category: str
    contact_email: str
    website: Optional[str]
    is_active: bool
    created_at: datetime

    @classmethod
    def from_entity(cls, entity: Supplier) -> "SupplierResponseDTO":
        return cls(
            id=entity.id,
            name=entity.name,
            country=entity.country,
            category=entity.category,
            contact_email=entity.contact_email,
            website=entity.website,
            is_active=entity.is_active,
            created_at=entity.created_at,
        )
