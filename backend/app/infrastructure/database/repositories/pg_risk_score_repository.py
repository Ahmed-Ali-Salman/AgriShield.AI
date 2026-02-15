"""
Infrastructure: PostgreSQL Risk Score Repository.
"""

from typing import List, Optional
from uuid import UUID
from dataclasses import asdict

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.risk_score import RiskScore
from app.domain.value_objects.score_signals import ScoreSignals
from app.domain.value_objects.risk_level import RiskLevel
from app.domain.interfaces.risk_score_repository import RiskScoreRepository
from app.infrastructure.database.models.risk_score_model import RiskScoreModel


class PgRiskScoreRepository(RiskScoreRepository):
    """PostgreSQL/SQLite implementation of RiskScoreRepository."""

    def __init__(self, session: AsyncSession):
        self._session = session

    def _to_entity(self, model: RiskScoreModel) -> RiskScore:
        signals = None
        if model.signals and isinstance(model.signals, dict):
            # Filter out class-level WEIGHT_ fields when reconstructing
            signal_fields = {
                k: v for k, v in model.signals.items()
                if not k.startswith("WEIGHT_")
            }
            signals = ScoreSignals(**signal_fields)

        return RiskScore(
            id=UUID(model.id) if isinstance(model.id, str) else model.id,
            supplier_id=UUID(model.supplier_id) if isinstance(model.supplier_id, str) else model.supplier_id,
            overall_score=model.overall_score,
            risk_level=RiskLevel(model.risk_level),
            signals=signals,
            computed_at=model.computed_at,
            notes=model.notes or "",
        )

    def _to_model(self, entity: RiskScore) -> RiskScoreModel:
        signals_dict = None
        if entity.signals:
            signals_dict = {
                "it_security_posture": entity.signals.it_security_posture,
                "data_consistency": entity.signals.data_consistency,
                "delivery_reliability": entity.signals.delivery_reliability,
                "compliance_audit": entity.signals.compliance_audit,
                "external_risk_factors": entity.signals.external_risk_factors,
            }

        return RiskScoreModel(
            id=str(entity.id),
            supplier_id=str(entity.supplier_id),
            overall_score=entity.overall_score,
            risk_level=entity.risk_level.value if isinstance(entity.risk_level, RiskLevel) else entity.risk_level,
            signals=signals_dict,
            computed_at=entity.computed_at,
            notes=entity.notes,
        )

    async def get_by_id(self, score_id: UUID) -> Optional[RiskScore]:
        result = await self._session.get(RiskScoreModel, str(score_id))
        return self._to_entity(result) if result else None

    async def get_latest_for_supplier(self, supplier_id: UUID) -> Optional[RiskScore]:
        stmt = (
            select(RiskScoreModel)
            .where(RiskScoreModel.supplier_id == str(supplier_id))
            .order_by(desc(RiskScoreModel.computed_at))
            .limit(1)
        )
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        return self._to_entity(row) if row else None

    async def get_history(self, supplier_id: UUID, limit: int = 30) -> List[RiskScore]:
        stmt = (
            select(RiskScoreModel)
            .where(RiskScoreModel.supplier_id == str(supplier_id))
            .order_by(desc(RiskScoreModel.computed_at))
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(row) for row in result.scalars().all()]

    async def create(self, risk_score: RiskScore) -> RiskScore:
        model = self._to_model(risk_score)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def get_high_risk_suppliers(self, threshold: float = 50.0) -> List[RiskScore]:
        stmt = (
            select(RiskScoreModel)
            .where(RiskScoreModel.overall_score >= threshold)
            .order_by(desc(RiskScoreModel.overall_score))
        )
        result = await self._session.execute(stmt)
        return [self._to_entity(row) for row in result.scalars().all()]
