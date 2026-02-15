"""
Application DTO: Risk Score Data Transfer Objects.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from app.domain.entities.risk_score import RiskScore
from app.domain.value_objects.risk_level import RiskLevel


@dataclass
class RiskScoreInputDTO:
    """Input DTO for computing a risk score."""
    it_security_posture: float = 0.0
    data_consistency: float = 0.0
    delivery_reliability: float = 0.0
    compliance_audit: float = 0.0
    external_risk_factors: float = 0.0


@dataclass
class RiskScoreResponseDTO:
    """Output DTO for risk scores."""
    id: UUID
    supplier_id: UUID
    overall_score: float
    risk_level: RiskLevel
    computed_at: datetime
    notes: str

    @classmethod
    def from_entity(cls, entity: RiskScore) -> "RiskScoreResponseDTO":
        return cls(
            id=entity.id,
            supplier_id=entity.supplier_id,
            overall_score=entity.overall_score,
            risk_level=entity.risk_level,
            computed_at=entity.computed_at,
            notes=entity.notes,
        )
