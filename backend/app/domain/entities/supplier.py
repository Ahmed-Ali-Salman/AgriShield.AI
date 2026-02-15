"""
Domain Entity: Supplier.

Represents a supplier in the food supply chain.
This is a pure domain object with no framework dependencies.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Supplier:
    """Core business entity representing a food supply chain supplier."""

    id: UUID = field(default_factory=uuid4)
    name: str = ""
    country: str = ""
    category: str = ""  # e.g. "grain", "dairy", "logistics"
    contact_email: str = ""
    website: Optional[str] = None
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # --- Business rules (Single Responsibility: entity validation) ---

    def deactivate(self) -> None:
        """Mark supplier as inactive."""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """Reactivate a previously deactivated supplier."""
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def is_valid(self) -> bool:
        """Basic domain validation."""
        return bool(self.name) and bool(self.country) and bool(self.category)
