"""
Domain Service: RiskScoringService.

Pure business logic for computing Cyber-Food Risk Scores.
This service has NO infrastructure dependencies — it operates
on domain entities and value objects only.
"""

from app.domain.entities.risk_score import RiskScore
from app.domain.entities.supplier import Supplier
from app.domain.value_objects.score_signals import ScoreSignals
from app.domain.value_objects.risk_level import RiskLevel


class RiskScoringService:
    """
    Computes the Cyber-Food Risk Score for a supplier.

    This is a domain service because the scoring logic spans
    multiple entities (Supplier + Anomalies + external signals)
    and doesn't naturally belong to a single entity.
    """

    def compute_score(self, signals: ScoreSignals) -> RiskScore:
        """
        Compute a RiskScore from signal inputs.

        Args:
            signals: The weighted signal breakdown.

        Returns:
            A fully populated RiskScore entity.
        """
        overall = signals.compute_overall()
        score = RiskScore(
            overall_score=round(overall, 2),
            signals=signals,
        )
        score.risk_level = score.classify()
        return score

    def build_signals(
        self,
        it_security: float = 0.0,
        data_consistency: float = 0.0,
        delivery: float = 0.0,
        compliance: float = 0.0,
        external: float = 0.0,
    ) -> ScoreSignals:
        """
        Construct a ScoreSignals value object from raw input data.

        Each input should be a float 0–100.
        In a full implementation, these values would be derived from
        data analysis, but for MVP they may be manually assessed.
        """
        return ScoreSignals(
            it_security_posture=max(0.0, min(100.0, it_security)),
            data_consistency=max(0.0, min(100.0, data_consistency)),
            delivery_reliability=max(0.0, min(100.0, delivery)),
            compliance_audit=max(0.0, min(100.0, compliance)),
            external_risk_factors=max(0.0, min(100.0, external)),
        )
