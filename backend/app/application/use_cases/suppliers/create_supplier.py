"""
Use Case: Create Supplier.

Single Responsibility: handles the creation of a new supplier.
"""

from uuid import UUID

from app.domain.entities.supplier import Supplier
from app.domain.interfaces.supplier_repository import SupplierRepository
from app.application.dto.supplier_dto import CreateSupplierDTO, SupplierResponseDTO


class CreateSupplierUseCase:
    """Orchestrates supplier creation."""

    def __init__(self, supplier_repo: SupplierRepository):
        self._supplier_repo = supplier_repo

    async def execute(self, dto: CreateSupplierDTO) -> SupplierResponseDTO:
        """Create a new supplier from the provided DTO."""
        supplier = Supplier(
            name=dto.name,
            country=dto.country,
            category=dto.category,
            contact_email=dto.contact_email,
            website=dto.website,
        )

        if not supplier.is_valid():
            raise ValueError("Supplier data is invalid: name, country, and category are required.")

        created = await self._supplier_repo.create(supplier)
        return SupplierResponseDTO.from_entity(created)
