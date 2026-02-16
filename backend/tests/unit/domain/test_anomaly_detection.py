"""Unit tests: Anomaly Detection Domain Service."""
import pytest
from app.domain.services.anomaly_detection_service import AnomalyDetectionService
from app.domain.entities.anomaly import AnomalyType


@pytest.fixture
def svc():
    return AnomalyDetectionService()


# ── Invoice Discrepancy ─────────────────────────────────────
class TestInvoiceDiscrepancy:
    def test_no_anomaly_within_threshold(self, svc):
        """A 10% deviation should be within the 30% threshold."""
        result = svc.check_invoice_discrepancy(100.0, 110.0, "s1")
        assert result is None

    def test_anomaly_above_threshold(self, svc):
        """A 50% deviation should trigger an anomaly."""
        result = svc.check_invoice_discrepancy(100.0, 150.0, "s1")
        assert result is not None
        assert result.anomaly_type == AnomalyType.INVOICE_DISCREPANCY
        assert result.confidence > 0

    def test_anomaly_below_expected(self, svc):
        """Actual < expected should also trigger if deviation > threshold."""
        result = svc.check_invoice_discrepancy(100.0, 50.0, "s1")
        assert result is not None
        assert result.anomaly_type == AnomalyType.INVOICE_DISCREPANCY

    def test_zero_expected_returns_none(self, svc):
        """Division by zero guard: expected_total=0."""
        result = svc.check_invoice_discrepancy(0.0, 100.0, "s1")
        assert result is None

    def test_exact_threshold_no_anomaly(self, svc):
        """Exactly at the 30% threshold should NOT trigger (> not >=)."""
        result = svc.check_invoice_discrepancy(100.0, 130.0, "s1")
        assert result is None

    def test_confidence_capped_at_1(self, svc):
        """Confidence should never exceed 1.0 even for extreme deviations."""
        result = svc.check_invoice_discrepancy(100.0, 500.0, "s1")
        assert result is not None
        assert result.confidence <= 1.0


# ── Quantity Deviation ──────────────────────────────────────
class TestQuantityDeviation:
    def test_no_anomaly_within_threshold(self, svc):
        """A 10% deviation should be within the 25% threshold."""
        result = svc.check_quantity_deviation(100.0, 110.0, "s1")
        assert result is None

    def test_anomaly_above_threshold(self, svc):
        """A 50% deviation should trigger an anomaly."""
        result = svc.check_quantity_deviation(100.0, 150.0, "s1")
        assert result is not None
        assert result.anomaly_type == AnomalyType.QUANTITY_DEVIATION

    def test_zero_historical_returns_none(self, svc):
        result = svc.check_quantity_deviation(0.0, 100.0, "s1")
        assert result is None


# ── Run All Checks ──────────────────────────────────────────
class TestRunAllChecks:
    def test_empty_data_returns_no_anomalies(self, svc):
        result = svc.run_all_checks({}, "s1")
        assert result == []

    def test_normal_data_returns_no_anomalies(self, svc):
        data = {
            "expected_total": 100.0,
            "actual_total": 110.0,
            "historical_avg_quantity": 100.0,
            "current_quantity": 105.0,
        }
        result = svc.run_all_checks(data, "s1")
        assert len(result) == 0

    def test_bad_data_returns_two_anomalies(self, svc):
        data = {
            "expected_total": 100.0,
            "actual_total": 200.0,
            "historical_avg_quantity": 100.0,
            "current_quantity": 300.0,
        }
        result = svc.run_all_checks(data, "s1")
        assert len(result) == 2
        types = {a.anomaly_type for a in result}
        assert AnomalyType.INVOICE_DISCREPANCY in types
        assert AnomalyType.QUANTITY_DEVIATION in types

    def test_partial_data_only_runs_relevant_check(self, svc):
        data = {"expected_total": 100.0, "actual_total": 200.0}
        result = svc.run_all_checks(data, "s1")
        assert len(result) == 1
        assert result[0].anomaly_type == AnomalyType.INVOICE_DISCREPANCY
