"""
Use Case: Calculate Risk Score.

Orchestrates the risk scoring process by combining domain services
with repository persistence.
"""

from uuid import UUID

from app.domain.interfaces.supplier_repository import SupplierRepository
from app.domain.interfaces.risk_score_repository import RiskScoreRepository
from app.domain.services.risk_scoring_service import RiskScoringService
from app.application.dto.risk_score_dto import RiskScoreInputDTO, RiskScoreResponseDTO


class CalculateRiskScoreUseCase:
    """Compute and persist a Cyber-Food Risk Score for a supplier."""

    def __init__(
        self,
        supplier_repo: SupplierRepository,
        risk_score_repo: RiskScoreRepository,
        scoring_service: RiskScoringService,
    ):
        self._supplier_repo = supplier_repo
        self._risk_score_repo = risk_score_repo
        self._scoring_service = scoring_service

    async def execute(self, supplier_id: UUID, dto: RiskScoreInputDTO) -> RiskScoreResponseDTO:
        # Verify supplier exists
        supplier = await self._supplier_repo.get_by_id(supplier_id)
        if supplier is None:
            raise ValueError(f"Supplier {supplier_id} not found.")

        # Build signals and compute score (pure domain logic)
        signals = self._scoring_service.build_signals(
            it_security=dto.it_security_posture,
            data_consistency=dto.data_consistency,
            delivery=dto.delivery_reliability,
            compliance=dto.compliance_audit,
            external=dto.external_risk_factors,
        )
        risk_score = self._scoring_service.compute_score(signals)
        risk_score.supplier_id = supplier_id

        # Persist the score
        saved = await self._risk_score_repo.create(risk_score)
        return RiskScoreResponseDTO.from_entity(saved)
