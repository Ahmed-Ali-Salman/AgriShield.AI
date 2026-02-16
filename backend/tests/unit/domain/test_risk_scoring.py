"""Unit tests: Risk Scoring Domain Service."""
import pytest
from app.domain.services.risk_scoring_service import RiskScoringService
from app.domain.value_objects.risk_level import RiskLevel


@pytest.fixture
def svc():
    return RiskScoringService()


# ── Score Classification ────────────────────────────────────
class TestScoreClassification:
    def test_all_zeros_gives_low_risk(self, svc):
        signals = svc.build_signals(0, 0, 0, 0, 0)
        score = svc.compute_score(signals)
        assert score.overall_score == 0.0
        assert score.risk_level == RiskLevel.LOW

    def test_all_low_values_gives_low_risk(self, svc):
        signals = svc.build_signals(10, 10, 10, 10, 10)
        score = svc.compute_score(signals)
        assert score.overall_score == 10.0
        assert score.risk_level == RiskLevel.LOW

    def test_medium_risk_range(self, svc):
        signals = svc.build_signals(35, 35, 35, 35, 35)
        score = svc.compute_score(signals)
        assert score.risk_level == RiskLevel.MEDIUM

    def test_high_risk_range(self, svc):
        signals = svc.build_signals(60, 60, 60, 60, 60)
        score = svc.compute_score(signals)
        assert score.risk_level == RiskLevel.HIGH

    def test_critical_risk_range(self, svc):
        signals = svc.build_signals(90, 90, 90, 90, 90)
        score = svc.compute_score(signals)
        assert score.overall_score == 90.0
        assert score.risk_level == RiskLevel.CRITICAL

    def test_boundary_low_medium(self, svc):
        """Score of 25 should be MEDIUM (LOW is 0-24)."""
        signals = svc.build_signals(25, 25, 25, 25, 25)
        score = svc.compute_score(signals)
        assert score.risk_level == RiskLevel.MEDIUM

    def test_boundary_medium_high(self, svc):
        """Score of 50 should be HIGH."""
        signals = svc.build_signals(50, 50, 50, 50, 50)
        score = svc.compute_score(signals)
        assert score.risk_level == RiskLevel.HIGH

    def test_boundary_high_critical(self, svc):
        """Score of 75 should be CRITICAL."""
        signals = svc.build_signals(75, 75, 75, 75, 75)
        score = svc.compute_score(signals)
        assert score.risk_level == RiskLevel.CRITICAL


# ── Signal Clamping ─────────────────────────────────────────
class TestSignalClamping:
    def test_negative_values_clamped_to_zero(self, svc):
        signals = svc.build_signals(-10, -20, -30, -40, -50)
        assert signals.it_security_posture == 0.0
        assert signals.data_consistency == 0.0

    def test_values_over_100_clamped(self, svc):
        signals = svc.build_signals(150, 200, 110, 120, 130)
        assert signals.it_security_posture == 100.0
        assert signals.data_consistency == 100.0
        assert signals.delivery_reliability == 100.0


# ── Weighted Scoring ────────────────────────────────────────
class TestWeightedScoring:
    def test_mixed_signals_produce_weighted_average(self, svc):
        """Different signal values should produce a weighted average, not arithmetic mean."""
        signals = svc.build_signals(100, 0, 0, 0, 0)
        score = svc.compute_score(signals)
        # Only IT security is high, so overall should be partial
        assert 0 < score.overall_score < 100

    def test_all_max_scores_100(self, svc):
        signals = svc.build_signals(100, 100, 100, 100, 100)
        score = svc.compute_score(signals)
        assert score.overall_score == 100.0

    def test_score_is_rounded(self, svc):
        signals = svc.build_signals(33, 33, 33, 33, 33)
        score = svc.compute_score(signals)
        # Should be rounded to 2 decimal places
        assert score.overall_score == round(score.overall_score, 2)
