"""
Infrastructure: Role-Based Access Control (RBAC).

Defines permission checks based on user roles.
"""

from enum import Enum
from typing import List

from app.domain.entities.user import UserRole


# Permission definitions
class Permission(str, Enum):
    VIEW_DASHBOARD = "view_dashboard"
    MANAGE_SUPPLIERS = "manage_suppliers"
    VIEW_RISK_SCORES = "view_risk_scores"
    COMPUTE_RISK_SCORES = "compute_risk_scores"
    MANAGE_ALERTS = "manage_alerts"
    MANAGE_USERS = "manage_users"
    UPLOAD_DATA = "upload_data"


# Role → Permission mapping
ROLE_PERMISSIONS: dict[UserRole, List[Permission]] = {
    UserRole.VIEWER: [
        Permission.VIEW_DASHBOARD,
        Permission.VIEW_RISK_SCORES,
    ],
    UserRole.ANALYST: [
        Permission.VIEW_DASHBOARD,
        Permission.VIEW_RISK_SCORES,
        Permission.MANAGE_SUPPLIERS,
        Permission.COMPUTE_RISK_SCORES,
        Permission.MANAGE_ALERTS,
        Permission.UPLOAD_DATA,
    ],
    UserRole.ADMIN: list(Permission),  # All permissions
}


def has_permission(role: UserRole, permission: Permission) -> bool:
    """Check if a role has a specific permission."""
    return permission in ROLE_PERMISSIONS.get(role, [])
