"""
Domain Service: AnomalyDetectionService.

Pure business logic for rule-based anomaly detection.
ML-based detection is in Infrastructure; this service defines
the domain rules and thresholds.
"""

from typing import Dict, Any, List

from app.domain.entities.anomaly import Anomaly, AnomalyType


class AnomalyDetectionService:
    """
    Rule-based anomaly detection for supplier data.

    This domain service applies business rules to detect anomalies.
    The ML-based anomaly detection lives in Infrastructure and
    feeds results into this service for domain-level classification.
    """

    # Configurable thresholds
    PRICE_DEVIATION_THRESHOLD: float = 0.30   # 30% deviation
    QUANTITY_DEVIATION_THRESHOLD: float = 0.25  # 25% deviation
    DELIVERY_DELAY_THRESHOLD_DAYS: int = 7

    def check_invoice_discrepancy(
        self, expected_total: float, actual_total: float, supplier_id: str
    ) -> Anomaly | None:
        """Flag invoices where actual differs significantly from expected."""
        if expected_total == 0:
            return None

        deviation = abs(actual_total - expected_total) / expected_total
        if deviation > self.PRICE_DEVIATION_THRESHOLD:
            return Anomaly(
                anomaly_type=AnomalyType.INVOICE_DISCREPANCY,
                confidence=min(deviation, 1.0),
                description=(
                    f"Invoice total deviation of {deviation:.1%}. "
                    f"Expected: {expected_total}, Actual: {actual_total}"
                ),
                raw_data={
                    "expected": expected_total,
                    "actual": actual_total,
                    "deviation": deviation,
                },
            )
        return None

    def check_quantity_deviation(
        self, historical_avg: float, current_quantity: float, supplier_id: str
    ) -> Anomaly | None:
        """Flag significant deviations from historical quantity averages."""
        if historical_avg == 0:
            return None

        deviation = abs(current_quantity - historical_avg) / historical_avg
        if deviation > self.QUANTITY_DEVIATION_THRESHOLD:
            return Anomaly(
                anomaly_type=AnomalyType.QUANTITY_DEVIATION,
                confidence=min(deviation, 1.0),
                description=(
                    f"Quantity deviation of {deviation:.1%} from historical average. "
                    f"Average: {historical_avg}, Current: {current_quantity}"
                ),
                raw_data={
                    "historical_avg": historical_avg,
                    "current": current_quantity,
                    "deviation": deviation,
                },
            )
        return None

    def run_all_checks(self, data: Dict[str, Any], supplier_id: str) -> List[Anomaly]:
        """Run all rule-based anomaly checks on a data payload."""
        anomalies: List[Anomaly] = []

        # Invoice check
        if "expected_total" in data and "actual_total" in data:
            result = self.check_invoice_discrepancy(
                data["expected_total"], data["actual_total"], supplier_id
            )
            if result:
                anomalies.append(result)

        # Quantity check
        if "historical_avg_quantity" in data and "current_quantity" in data:
            result = self.check_quantity_deviation(
                data["historical_avg_quantity"], data["current_quantity"], supplier_id
            )
            if result:
                anomalies.append(result)

        return anomalies
