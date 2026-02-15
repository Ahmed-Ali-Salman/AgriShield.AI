"""
Domain Entity: RiskScore.

Represents a computed Cyber-Food Risk Score for a supplier.
Scores range from 0 (lowest risk) to 100 (highest risk).
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from app.domain.value_objects.score_signals import ScoreSignals
from app.domain.value_objects.risk_level import RiskLevel


@dataclass
class RiskScore:
    """A point-in-time Cyber-Food Risk Score for a specific supplier."""

    id: UUID = field(default_factory=uuid4)
    supplier_id: UUID = field(default_factory=uuid4)
    overall_score: float = 0.0  # 0–100
    risk_level: RiskLevel = RiskLevel.LOW
    signals: Optional[ScoreSignals] = None
    computed_at: datetime = field(default_factory=datetime.utcnow)
    notes: str = ""

    # --- Business logic ---

    def classify(self) -> RiskLevel:
        """Derive risk level from the numerical score."""
        if self.overall_score >= 75:
            return RiskLevel.CRITICAL
        elif self.overall_score >= 50:
            return RiskLevel.HIGH
        elif self.overall_score >= 25:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def is_actionable(self) -> bool:
        """Returns True if the score warrants an alert."""
        return self.overall_score >= 50
