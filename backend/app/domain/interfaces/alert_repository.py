"""
Domain Interface: AlertRepository.

Abstract contract for alert persistence.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from app.domain.entities.alert import Alert, AlertStatus


class AlertRepository(ABC):
    """Abstract repository for Alert entity persistence."""

    @abstractmethod
    async def get_by_id(self, alert_id: UUID) -> Optional[Alert]:
        ...

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 50) -> List[Alert]:
        ...

    @abstractmethod
    async def get_by_status(self, status: AlertStatus) -> List[Alert]:
        ...

    @abstractmethod
    async def get_by_supplier(self, supplier_id: UUID) -> List[Alert]:
        ...

    @abstractmethod
    async def create(self, alert: Alert) -> Alert:
        ...

    @abstractmethod
    async def update(self, alert: Alert) -> Alert:
        ...

    @abstractmethod
    async def count_open(self) -> int:
        """Count currently open alerts."""
        ...
