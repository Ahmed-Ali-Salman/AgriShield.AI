"""
Application DTO: Alert Data Transfer Objects.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from app.domain.entities.alert import Alert, AlertSeverity, AlertStatus


@dataclass
class CreateAlertDTO:
    """Input DTO for creating an alert."""
    supplier_id: UUID
    title: str
    description: str
    severity: AlertSeverity = AlertSeverity.INFO


@dataclass
class AlertResponseDTO:
    """Output DTO for alerts."""
    id: UUID
    supplier_id: UUID
    title: str
    description: str
    severity: AlertSeverity
    status: AlertStatus
    triggered_at: datetime
    resolved_at: Optional[datetime]

    @classmethod
    def from_entity(cls, entity: Alert) -> "AlertResponseDTO":
        return cls(
            id=entity.id,
            supplier_id=entity.supplier_id,
            title=entity.title,
            description=entity.description,
            severity=entity.severity,
            status=entity.status,
            triggered_at=entity.triggered_at,
            resolved_at=entity.resolved_at,
        )
