"""
Infrastructure Service: Email Notification.

Concrete implementation of NotificationService using SMTP.
"""

from typing import List

from app.application.interfaces.notification_service import NotificationService
from app.config import settings


class EmailNotificationService(NotificationService):
    """Sends notifications via email (SMTP)."""

    async def send(self, recipients: List[str], subject: str, body: str) -> bool:
        """
        Send an email notification.

        In MVP, this is a placeholder that logs the intent.
        Full SMTP implementation added in Phase 2.
        """
        # TODO: Implement SMTP sending via `emails` library
        print(f"[EMAIL] To: {recipients}, Subject: {subject}")
        return True
