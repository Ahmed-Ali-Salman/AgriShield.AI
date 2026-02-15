"""
Use Case: Update Supplier.
"""

from uuid import UUID

from app.domain.interfaces.supplier_repository import SupplierRepository
from app.application.dto.supplier_dto import UpdateSupplierDTO, SupplierResponseDTO


class UpdateSupplierUseCase:
    """Update an existing supplier's data."""

    def __init__(self, supplier_repo: SupplierRepository):
        self._supplier_repo = supplier_repo

    async def execute(self, supplier_id: UUID, dto: UpdateSupplierDTO) -> SupplierResponseDTO:
        supplier = await self._supplier_repo.get_by_id(supplier_id)
        if supplier is None:
            raise ValueError(f"Supplier {supplier_id} not found.")

        if dto.name is not None:
            supplier.name = dto.name
        if dto.country is not None:
            supplier.country = dto.country
        if dto.category is not None:
            supplier.category = dto.category
        if dto.contact_email is not None:
            supplier.contact_email = dto.contact_email
        if dto.website is not None:
            supplier.website = dto.website

        updated = await self._supplier_repo.update(supplier)
        return SupplierResponseDTO.from_entity(updated)
