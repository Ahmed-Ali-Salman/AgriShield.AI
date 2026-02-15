"""
Use Case: Create Alert.
"""

from app.domain.entities.alert import Alert
from app.domain.interfaces.alert_repository import AlertRepository
from app.application.interfaces.notification_service import NotificationService
from app.application.dto.alert_dto import CreateAlertDTO, AlertResponseDTO


class CreateAlertUseCase:
    """Create an alert and optionally send notifications."""

    def __init__(self, alert_repo: AlertRepository, notification_service: NotificationService = None):
        self._alert_repo = alert_repo
        self._notification_service = notification_service

    async def execute(self, dto: CreateAlertDTO, notify_emails: list[str] = None) -> AlertResponseDTO:
        alert = Alert(
            supplier_id=dto.supplier_id,
            title=dto.title,
            description=dto.description,
            severity=dto.severity,
        )

        saved = await self._alert_repo.create(alert)

        # Optionally send notification
        if self._notification_service and notify_emails:
            await self._notification_service.send(
                recipients=notify_emails,
                subject=f"[AgriShield Alert] {alert.severity.value.upper()}: {alert.title}",
                body=alert.description,
            )

        return AlertResponseDTO.from_entity(saved)
