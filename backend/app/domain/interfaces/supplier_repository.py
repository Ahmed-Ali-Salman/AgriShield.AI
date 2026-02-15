"""
Domain Interface: SupplierRepository.

Abstract contract for supplier persistence.
Infrastructure layer provides the concrete implementation (Dependency Inversion).
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.supplier import Supplier


class SupplierRepository(ABC):
    """Abstract repository for Supplier entity persistence."""

    @abstractmethod
    async def get_by_id(self, supplier_id: UUID) -> Optional[Supplier]:
        """Retrieve a supplier by its unique ID."""
        ...

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Supplier]:
        """Retrieve all suppliers with pagination."""
        ...

    @abstractmethod
    async def create(self, supplier: Supplier) -> Supplier:
        """Persist a new supplier."""
        ...

    @abstractmethod
    async def update(self, supplier: Supplier) -> Supplier:
        """Update an existing supplier."""
        ...

    @abstractmethod
    async def delete(self, supplier_id: UUID) -> bool:
        """Delete a supplier by ID. Returns True if deleted."""
        ...

    @abstractmethod
    async def get_by_category(self, category: str) -> List[Supplier]:
        """Retrieve all suppliers in a specific category."""
        ...

    @abstractmethod
    async def count(self) -> int:
        """Return total number of suppliers."""
        ...
