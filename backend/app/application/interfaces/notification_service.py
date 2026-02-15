"""
Application Interface: NotificationService.

Abstract interface for sending notifications (email, SMS, webhook).
Concrete implementations live in Infrastructure (Interface Segregation).
"""

from abc import ABC, abstractmethod
from typing import List


class NotificationService(ABC):
    """Abstract notification service — can be email, SMS, or webhook."""

    @abstractmethod
    async def send(self, recipients: List[str], subject: str, body: str) -> bool:
        """Send a notification. Returns True if successful."""
        ...
