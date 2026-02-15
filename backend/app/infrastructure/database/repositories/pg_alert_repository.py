"""
Infrastructure: PostgreSQL Alert Repository.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.alert import Alert, AlertSeverity, AlertStatus
from app.domain.interfaces.alert_repository import AlertRepository
from app.infrastructure.database.models.alert_model import AlertModel


class PgAlertRepository(AlertRepository):
    """PostgreSQL/SQLite implementation of AlertRepository."""

    def __init__(self, session: AsyncSession):
        self._session = session

    def _to_entity(self, model: AlertModel) -> Alert:
        return Alert(
            id=UUID(model.id) if isinstance(model.id, str) else model.id,
            supplier_id=UUID(model.supplier_id) if isinstance(model.supplier_id, str) else model.supplier_id,
            title=model.title,
            description=model.description or "",
            severity=AlertSeverity(model.severity) if model.severity else AlertSeverity.INFO,
            status=AlertStatus(model.status) if model.status else AlertStatus.OPEN,
            triggered_at=model.triggered_at,
            resolved_at=model.resolved_at,
        )

    def _to_model(self, entity: Alert) -> AlertModel:
        return AlertModel(
            id=str(entity.id),
            supplier_id=str(entity.supplier_id),
            title=entity.title,
            description=entity.description,
            severity=entity.severity.value if isinstance(entity.severity, AlertSeverity) else entity.severity,
            status=entity.status.value if isinstance(entity.status, AlertStatus) else entity.status,
            triggered_at=entity.triggered_at,
            resolved_at=entity.resolved_at,
        )

    async def get_by_id(self, alert_id: UUID) -> Optional[Alert]:
        result = await self._session.get(AlertModel, str(alert_id))
        return self._to_entity(result) if result else None

    async def get_by_status(self, status: str, skip: int = 0, limit: int = 50) -> List[Alert]:
        stmt = select(AlertModel).where(AlertModel.status == status).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return [self._to_entity(row) for row in result.scalars().all()]

    async def get_by_supplier(self, supplier_id: UUID) -> List[Alert]:
        stmt = select(AlertModel).where(AlertModel.supplier_id == str(supplier_id))
        result = await self._session.execute(stmt)
        return [self._to_entity(row) for row in result.scalars().all()]

    async def get_all(self, skip: int = 0, limit: int = 50) -> List[Alert]:
        stmt = select(AlertModel).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return [self._to_entity(row) for row in result.scalars().all()]

    async def create(self, alert: Alert) -> Alert:
        model = self._to_model(alert)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def update(self, alert: Alert) -> Alert:
        model = await self._session.get(AlertModel, str(alert.id))
        if model:
            model.status = alert.status.value if isinstance(alert.status, AlertStatus) else alert.status
            model.resolved_at = alert.resolved_at
            await self._session.flush()
        return self._to_entity(model)

    async def count_open(self) -> int:
        stmt = select(func.count()).select_from(AlertModel).where(AlertModel.status == "open")
        result = await self._session.execute(stmt)
        return result.scalar_one()
