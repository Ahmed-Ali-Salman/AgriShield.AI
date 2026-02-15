"""
Use Case: List Suppliers.
"""

from typing import List

from app.domain.interfaces.supplier_repository import SupplierRepository
from app.application.dto.supplier_dto import SupplierResponseDTO


class ListSuppliersUseCase:
    """Retrieve a paginated list of suppliers."""

    def __init__(self, supplier_repo: SupplierRepository):
        self._supplier_repo = supplier_repo

    async def execute(self, skip: int = 0, limit: int = 100) -> List[SupplierResponseDTO]:
        suppliers = await self._supplier_repo.get_all(skip=skip, limit=limit)
        return [SupplierResponseDTO.from_entity(s) for s in suppliers]
