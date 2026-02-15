"""
Application Interface: AuthService.

Abstract interface for authentication operations (password hashing, token creation).
Concrete implementation in Infrastructure/security.
"""

from abc import ABC, abstractmethod


class AuthService(ABC):
    """Abstract authentication service."""

    @abstractmethod
    def hash_password(self, password: str) -> str:
        ...

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        ...

    @abstractmethod
    def create_access_token(self, user_id: str, role: str) -> str:
        ...

    @abstractmethod
    def create_refresh_token(self, user_id: str) -> str:
        ...

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        ...
