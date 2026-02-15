"""
Presentation: Auth Dependency.

Extracts and validates the current user from the JWT token.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.domain.entities.user import User, UserRole
from app.infrastructure.security.jwt_handler import JWTAuthService
from app.infrastructure.security.rbac import Permission, has_permission

security_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> dict:
    """Extract user info from JWT token."""
    auth_service = JWTAuthService()
    try:
        payload = auth_service.decode_token(credentials.credentials)
        return {
            "user_id": payload["sub"],
            "role": UserRole(payload.get("role", "viewer")),
        }
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )


def require_permission(permission: Permission):
    """Dependency that checks if the current user has a specific permission."""

    async def checker(current_user: dict = Depends(get_current_user)):
        if not has_permission(current_user["role"], permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required: {permission.value}",
            )
        return current_user

    return checker
