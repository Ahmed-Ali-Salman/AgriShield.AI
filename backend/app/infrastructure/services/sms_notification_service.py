"""
Infrastructure Service: SMS Notification.

Concrete implementation of NotificationService using Twilio.
"""

from typing import List

from app.application.interfaces.notification_service import NotificationService
from app.config import settings


class SMSNotificationService(NotificationService):
    """Sends notifications via SMS (Twilio)."""

    async def send(self, recipients: List[str], subject: str, body: str) -> bool:
        """
        Send an SMS notification.

        In MVP, this is a placeholder.
        Full Twilio implementation added in Phase 2.
        """
        # TODO: Implement Twilio SMS sending
        print(f"[SMS] To: {recipients}, Message: {subject} - {body}")
        return True
