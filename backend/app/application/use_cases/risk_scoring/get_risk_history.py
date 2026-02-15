"""
Use Case: Get Risk Score History.
"""

from typing import List
from uuid import UUID

from app.domain.interfaces.risk_score_repository import RiskScoreRepository
from app.application.dto.risk_score_dto import RiskScoreResponseDTO


class GetRiskHistoryUseCase:
    """Retrieve the risk score history for a supplier."""

    def __init__(self, risk_score_repo: RiskScoreRepository):
        self._risk_score_repo = risk_score_repo

    async def execute(self, supplier_id: UUID, limit: int = 30) -> List[RiskScoreResponseDTO]:
        scores = await self._risk_score_repo.get_history(supplier_id, limit=limit)
        return [RiskScoreResponseDTO.from_entity(s) for s in scores]
