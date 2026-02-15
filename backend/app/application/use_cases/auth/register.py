"""
Use Case: Register.
"""

from app.domain.entities.user import User
from app.domain.interfaces.user_repository import UserRepository
from app.application.dto.auth_dto import RegisterDTO, TokenResponseDTO
from app.application.interfaces.auth_service import AuthService


class RegisterUseCase:
    """Register a new user."""

    def __init__(self, user_repo: UserRepository, auth_service: AuthService):
        self._user_repo = user_repo
        self._auth_service = auth_service

    async def execute(self, dto: RegisterDTO) -> TokenResponseDTO:
        existing = await self._user_repo.get_by_email(dto.email)
        if existing is not None:
            raise ValueError("A user with this email already exists.")

        hashed = self._auth_service.hash_password(dto.password)
        user = User(
            email=dto.email,
            hashed_password=hashed,
            full_name=dto.full_name,
            role=dto.role,
        )

        created = await self._user_repo.create(user)

        access_token = self._auth_service.create_access_token(str(created.id), created.role.value)
        refresh_token = self._auth_service.create_refresh_token(str(created.id))

        return TokenResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=created.id,
            role=created.role,
        )
