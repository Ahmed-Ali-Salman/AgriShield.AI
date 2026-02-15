"""
Infrastructure: PostgreSQL Anomaly Repository.
"""

from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.anomaly import Anomaly
from app.domain.interfaces.anomaly_repository import AnomalyRepository
from app.infrastructure.database.models.anomaly_model import AnomalyModel


class PgAnomalyRepository(AnomalyRepository):
    """PostgreSQL/SQLite implementation of AnomalyRepository."""

    def __init__(self, session: AsyncSession):
        self._session = session

    def _to_entity(self, model: AnomalyModel) -> Anomaly:
        return Anomaly(
            id=UUID(model.id) if isinstance(model.id, str) else model.id,
            supplier_id=UUID(model.supplier_id) if isinstance(model.supplier_id, str) else model.supplier_id,
            anomaly_type=model.anomaly_type,
            confidence=model.confidence,
            description=model.description or "",
            raw_data=model.raw_data,
            detected_at=model.detected_at,
            is_confirmed=model.is_confirmed,
        )

    def _to_model(self, entity: Anomaly) -> AnomalyModel:
        return AnomalyModel(
            id=str(entity.id),
            supplier_id=str(entity.supplier_id),
            anomaly_type=entity.anomaly_type,
            confidence=entity.confidence,
            description=entity.description,
            raw_data=entity.raw_data,
            detected_at=entity.detected_at,
            is_confirmed=entity.is_confirmed,
        )

    async def get_by_id(self, anomaly_id: UUID) -> Optional[Anomaly]:
        result = await self._session.get(AnomalyModel, str(anomaly_id))
        return self._to_entity(result) if result else None

    async def get_by_supplier(self, supplier_id: UUID) -> List[Anomaly]:
        stmt = select(AnomalyModel).where(AnomalyModel.supplier_id == str(supplier_id))
        result = await self._session.execute(stmt)
        return [self._to_entity(row) for row in result.scalars().all()]

    async def get_unreviewed(self) -> List[Anomaly]:
        stmt = select(AnomalyModel).where(AnomalyModel.is_confirmed.is_(None))
        result = await self._session.execute(stmt)
        return [self._to_entity(row) for row in result.scalars().all()]

    async def create(self, anomaly: Anomaly) -> Anomaly:
        model = self._to_model(anomaly)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def update(self, anomaly: Anomaly) -> Anomaly:
        model = await self._session.get(AnomalyModel, str(anomaly.id))
        if model:
            model.is_confirmed = anomaly.is_confirmed
            await self._session.flush()
        return self._to_entity(model)

    async def bulk_create(self, anomalies: List[Anomaly]) -> List[Anomaly]:
        models = [self._to_model(a) for a in anomalies]
        self._session.add_all(models)
        await self._session.flush()
        return [self._to_entity(m) for m in models]
