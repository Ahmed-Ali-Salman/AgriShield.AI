"""
Shared: Custom Exceptions.

Domain-specific exceptions used across all layers.
"""


class AgriShieldError(Exception):
    """Base exception for all AgriShield errors."""
    pass


class EntityNotFoundError(AgriShieldError):
    """Raised when an entity is not found by its ID."""
    def __init__(self, entity_type: str, entity_id: str):
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} with ID '{entity_id}' not found.")


class AuthenticationError(AgriShieldError):
    """Raised on authentication failures (bad credentials, expired token)."""
    pass


class AuthorizationError(AgriShieldError):
    """Raised when a user lacks permission for an action."""
    def __init__(self, required_permission: str):
        super().__init__(f"Insufficient permissions. Required: {required_permission}")


class ValidationError(AgriShieldError):
    """Raised on domain validation failures."""
    pass


class DataIngestionError(AgriShieldError):
    """Raised on file parsing or data ingestion failures."""
    pass
