"""
Use Case: Login.
"""

from app.domain.interfaces.user_repository import UserRepository
from app.application.dto.auth_dto import LoginDTO, TokenResponseDTO
from app.application.interfaces.auth_service import AuthService


class LoginUseCase:
    """Authenticate a user and return tokens."""

    def __init__(self, user_repo: UserRepository, auth_service: AuthService):
        self._user_repo = user_repo
        self._auth_service = auth_service

    async def execute(self, dto: LoginDTO) -> TokenResponseDTO:
        user = await self._user_repo.get_by_email(dto.email)
        if user is None:
            raise ValueError("Invalid email or password.")

        if not self._auth_service.verify_password(dto.password, user.hashed_password):
            raise ValueError("Invalid email or password.")

        access_token = self._auth_service.create_access_token(str(user.id), user.role.value)
        refresh_token = self._auth_service.create_refresh_token(str(user.id))

        return TokenResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
            role=user.role,
        )
