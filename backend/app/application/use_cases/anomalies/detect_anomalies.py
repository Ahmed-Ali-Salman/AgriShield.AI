"""
Use Case: Detect Anomalies.

Runs both rule-based and ML-based anomaly detection on supplier data.
"""

from typing import Dict, Any, List
from uuid import UUID

from app.domain.services.anomaly_detection_service import AnomalyDetectionService
from app.domain.interfaces.anomaly_repository import AnomalyRepository
from app.application.dto.risk_score_dto import RiskScoreResponseDTO


class DetectAnomaliesUseCase:
    """Run anomaly detection checks on supplier data."""

    def __init__(
        self,
        anomaly_detection_service: AnomalyDetectionService,
        anomaly_repo: AnomalyRepository,
    ):
        self._detection_service = anomaly_detection_service
        self._anomaly_repo = anomaly_repo

    async def execute(self, supplier_id: UUID, data: Dict[str, Any]) -> int:
        """
        Run all anomaly checks and persist the results.

        Returns:
            Number of anomalies detected.
        """
        anomalies = self._detection_service.run_all_checks(data, str(supplier_id))

        # Assign supplier ID to all detected anomalies
        for anomaly in anomalies:
            anomaly.supplier_id = supplier_id

        if anomalies:
            await self._anomaly_repo.bulk_create(anomalies)

        return len(anomalies)
