"""Unit tests: Risk Scoring Domain Service."""
from app.domain.services.risk_scoring_service import RiskScoringService
from app.domain.value_objects.risk_level import RiskLevel

def test_compute_low_risk():
    svc = RiskScoringService()
    signals = svc.build_signals(it_security=10, data_consistency=10, delivery=10, compliance=10, external=10)
    score = svc.compute_score(signals)
    assert score.overall_score == 10.0
    assert score.risk_level == RiskLevel.LOW

def test_compute_critical_risk():
    svc = RiskScoringService()
    signals = svc.build_signals(it_security=90, data_consistency=90, delivery=90, compliance=90, external=90)
    score = svc.compute_score(signals)
    assert score.overall_score == 90.0
    assert score.risk_level == RiskLevel.CRITICAL
