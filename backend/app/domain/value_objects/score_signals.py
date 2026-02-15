"""
Domain Value Object: ScoreSignals.

Immutable value object representing the weighted signal breakdown
that composes a Cyber-Food Risk Score.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ScoreSignals:
    """
    Breakdown of signals contributing to a supplier's risk score.

    Each signal is a float 0–100 representing the risk in that category.
    The overall score is a weighted combination of these signals.

    Weights:
        - IT Security Posture:    25%
        - Data Consistency:       25%
        - Delivery Reliability:   25%
        - Compliance & Audit:     15%
        - External Risk Factors:  10%
    """

    it_security_posture: float = 0.0
    data_consistency: float = 0.0
    delivery_reliability: float = 0.0
    compliance_audit: float = 0.0
    external_risk_factors: float = 0.0

    # Weights as class-level constants
    WEIGHT_IT_SECURITY: float = 0.25
    WEIGHT_DATA_CONSISTENCY: float = 0.25
    WEIGHT_DELIVERY: float = 0.25
    WEIGHT_COMPLIANCE: float = 0.15
    WEIGHT_EXTERNAL: float = 0.10

    def compute_overall(self) -> float:
        """Compute the weighted overall risk score."""
        return (
            self.it_security_posture * self.WEIGHT_IT_SECURITY
            + self.data_consistency * self.WEIGHT_DATA_CONSISTENCY
            + self.delivery_reliability * self.WEIGHT_DELIVERY
            + self.compliance_audit * self.WEIGHT_COMPLIANCE
            + self.external_risk_factors * self.WEIGHT_EXTERNAL
        )
