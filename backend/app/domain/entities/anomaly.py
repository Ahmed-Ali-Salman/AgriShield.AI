"""
Domain Entity: Anomaly.

Represents a detected anomaly in supplier data or behavior.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional
from uuid import UUID, uuid4


class AnomalyType(str, Enum):
    INVOICE_DISCREPANCY = "invoice_discrepancy"
    QUANTITY_DEVIATION = "quantity_deviation"
    DELIVERY_PATTERN = "delivery_pattern"
    PRICE_SPIKE = "price_spike"
    BEHAVIORAL = "behavioral"


@dataclass
class Anomaly:
    """A detected anomaly flagged by the ML engine or rule-based system."""

    id: UUID = field(default_factory=uuid4)
    supplier_id: UUID = field(default_factory=uuid4)
    anomaly_type: AnomalyType = AnomalyType.BEHAVIORAL
    confidence: float = 0.0  # 0.0–1.0
    description: str = ""
    raw_data: Dict[str, Any] = field(default_factory=dict)
    detected_at: datetime = field(default_factory=datetime.utcnow)
    is_confirmed: Optional[bool] = None  # None = unreviewed

    def confirm(self) -> None:
        """Human analyst confirms this anomaly is real."""
        self.is_confirmed = True

    def dismiss(self) -> None:
        """Human analyst dismisses this as a false positive."""
        self.is_confirmed = False

    def is_high_confidence(self) -> bool:
        return self.confidence >= 0.8
