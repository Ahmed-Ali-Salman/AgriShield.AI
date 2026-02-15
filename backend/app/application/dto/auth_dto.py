"""
Application DTO: Auth Data Transfer Objects.
"""

from dataclasses import dataclass
from uuid import UUID

from app.domain.entities.user import UserRole


@dataclass
class RegisterDTO:
    """Input DTO for user registration."""
    email: str
    password: str
    full_name: str
    role: UserRole = UserRole.VIEWER


@dataclass
class LoginDTO:
    """Input DTO for login."""
    email: str
    password: str


@dataclass
class TokenResponseDTO:
    """Output DTO for authentication tokens."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: UUID = None
    role: UserRole = UserRole.VIEWER
