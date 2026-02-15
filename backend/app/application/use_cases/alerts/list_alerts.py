"""
Use Case: List Alerts.
"""

from typing import List

from app.domain.interfaces.alert_repository import AlertRepository
from app.domain.entities.alert import AlertStatus
from app.application.dto.alert_dto import AlertResponseDTO


class ListAlertsUseCase:
    """Retrieve alerts with optional filtering."""

    def __init__(self, alert_repo: AlertRepository):
        self._alert_repo = alert_repo

    async def execute(self, status: AlertStatus = None, skip: int = 0, limit: int = 50) -> List[AlertResponseDTO]:
        if status:
            alerts = await self._alert_repo.get_by_status(status)
        else:
            alerts = await self._alert_repo.get_all(skip=skip, limit=limit)
        return [AlertResponseDTO.from_entity(a) for a in alerts]
