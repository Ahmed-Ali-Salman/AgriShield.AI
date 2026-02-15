"""
Infrastructure: PostgreSQL Supplier Repository.

Concrete implementation of the SupplierRepository interface.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.supplier import Supplier
from app.domain.interfaces.supplier_repository import SupplierRepository
from app.infrastructure.database.models.supplier_model import SupplierModel


class PgSupplierRepository(SupplierRepository):
    """PostgreSQL/SQLite implementation of SupplierRepository."""

    def __init__(self, session: AsyncSession):
        self._session = session

    def _to_entity(self, model: SupplierModel) -> Supplier:
        """Map ORM model to domain entity."""
        return Supplier(
            id=UUID(model.id) if isinstance(model.id, str) else model.id,
            name=model.name,
            country=model.country,
            category=model.category,
            contact_email=model.contact_email,
            website=model.website or "",
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: Supplier) -> SupplierModel:
        """Map domain entity to ORM model."""
        return SupplierModel(
            id=str(entity.id),
            name=entity.name,
            country=entity.country,
            category=entity.category,
            contact_email=entity.contact_email,
            website=entity.website,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def get_by_id(self, supplier_id: UUID) -> Optional[Supplier]:
        result = await self._session.get(SupplierModel, str(supplier_id))
        return self._to_entity(result) if result else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Supplier]:
        stmt = select(SupplierModel).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return [self._to_entity(row) for row in result.scalars().all()]

    async def create(self, supplier: Supplier) -> Supplier:
        model = self._to_model(supplier)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def update(self, supplier: Supplier) -> Supplier:
        model = await self._session.get(SupplierModel, str(supplier.id))
        if model:
            model.name = supplier.name
            model.country = supplier.country
            model.category = supplier.category
            model.contact_email = supplier.contact_email
            model.website = supplier.website
            model.is_active = supplier.is_active
            model.updated_at = supplier.updated_at
            await self._session.flush()
        return self._to_entity(model)

    async def delete(self, supplier_id: UUID) -> bool:
        model = await self._session.get(SupplierModel, str(supplier_id))
        if model:
            await self._session.delete(model)
            return True
        return False

    async def get_by_category(self, category: str) -> List[Supplier]:
        stmt = select(SupplierModel).where(SupplierModel.category == category)
        result = await self._session.execute(stmt)
        return [self._to_entity(row) for row in result.scalars().all()]

    async def count(self) -> int:
        stmt = select(func.count()).select_from(SupplierModel)
        result = await self._session.execute(stmt)
        return result.scalar_one()
