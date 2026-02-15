"""
Use Case: Get Supplier.
"""

from typing import Optional
from uuid import UUID

from app.domain.interfaces.supplier_repository import SupplierRepository
from app.application.dto.supplier_dto import SupplierResponseDTO


class GetSupplierUseCase:
    """Retrieve a single supplier by ID."""

    def __init__(self, supplier_repo: SupplierRepository):
        self._supplier_repo = supplier_repo

    async def execute(self, supplier_id: UUID) -> Optional[SupplierResponseDTO]:
        supplier = await self._supplier_repo.get_by_id(supplier_id)
        if supplier is None:
            return None
        return SupplierResponseDTO.from_entity(supplier)
