"""
Use Case: Get Anomalies.
"""

from typing import List
from uuid import UUID

from app.domain.interfaces.anomaly_repository import AnomalyRepository
from app.domain.entities.anomaly import Anomaly


class GetAnomaliesUseCase:
    """Retrieve anomalies for a supplier or unreviewed anomalies."""

    def __init__(self, anomaly_repo: AnomalyRepository):
        self._anomaly_repo = anomaly_repo

    async def get_by_supplier(self, supplier_id: UUID) -> List[Anomaly]:
        return await self._anomaly_repo.get_by_supplier(supplier_id)

    async def get_unreviewed(self) -> List[Anomaly]:
        return await self._anomaly_repo.get_unreviewed()
