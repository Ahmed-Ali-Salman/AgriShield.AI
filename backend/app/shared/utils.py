"""
Shared: Utility Functions.
"""

from datetime import datetime
from uuid import UUID


def is_valid_uuid(value: str) -> bool:
    """Check if a string is a valid UUID."""
    try:
        UUID(value)
        return True
    except ValueError:
        return False


def format_datetime(dt: datetime) -> str:
    """Format datetime for API responses."""
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
