"""
Domain Entity: User.

Represents an authenticated platform user.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


class UserRole(str, Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"


@dataclass
class User:
    """A registered user of the AgriShield AI platform."""

    id: UUID = field(default_factory=uuid4)
    email: str = ""
    hashed_password: str = ""
    full_name: str = ""
    role: UserRole = UserRole.VIEWER
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)

    def has_permission(self, required_role: UserRole) -> bool:
        """Check if user has at least the required role level."""
        role_hierarchy = {UserRole.VIEWER: 0, UserRole.ANALYST: 1, UserRole.ADMIN: 2}
        return role_hierarchy.get(self.role, 0) >= role_hierarchy.get(required_role, 0)
