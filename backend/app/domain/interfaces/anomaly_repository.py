"""
Domain Interface: AnomalyRepository.

Abstract contract for anomaly persistence.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.anomaly import Anomaly


class AnomalyRepository(ABC):
    """Abstract repository for Anomaly entity persistence."""

    @abstractmethod
    async def get_by_id(self, anomaly_id: UUID) -> Optional[Anomaly]:
        ...

    @abstractmethod
    async def get_by_supplier(self, supplier_id: UUID) -> List[Anomaly]:
        ...

    @abstractmethod
    async def get_unreviewed(self) -> List[Anomaly]:
        """Get anomalies that haven't been confirmed or dismissed."""
        ...

    @abstractmethod
    async def create(self, anomaly: Anomaly) -> Anomaly:
        ...

    @abstractmethod
    async def update(self, anomaly: Anomaly) -> Anomaly:
        ...

    @abstractmethod
    async def bulk_create(self, anomalies: List[Anomaly]) -> List[Anomaly]:
        """Persist multiple anomalies at once (batch detection results)."""
        ...
