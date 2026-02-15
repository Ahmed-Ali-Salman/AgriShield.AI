"""
Domain Interface: RiskScoreRepository.

Abstract contract for risk score persistence.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.risk_score import RiskScore


class RiskScoreRepository(ABC):
    """Abstract repository for RiskScore entity persistence."""

    @abstractmethod
    async def get_by_id(self, score_id: UUID) -> Optional[RiskScore]:
        ...

    @abstractmethod
    async def get_latest_for_supplier(self, supplier_id: UUID) -> Optional[RiskScore]:
        """Get the most recent risk score for a supplier."""
        ...

    @abstractmethod
    async def get_history(self, supplier_id: UUID, limit: int = 30) -> List[RiskScore]:
        """Get risk score history for a supplier (most recent first)."""
        ...

    @abstractmethod
    async def create(self, risk_score: RiskScore) -> RiskScore:
        ...

    @abstractmethod
    async def get_high_risk_suppliers(self, threshold: float = 50.0) -> List[RiskScore]:
        """Get all suppliers with scores above the threshold."""
        ...
