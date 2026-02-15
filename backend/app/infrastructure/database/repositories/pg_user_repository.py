"""
Infrastructure: PostgreSQL User Repository.
"""

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.user import User, UserRole
from app.domain.interfaces.user_repository import UserRepository
from app.infrastructure.database.models.user_model import UserModel


class PgUserRepository(UserRepository):
    """PostgreSQL/SQLite implementation of UserRepository."""

    def __init__(self, session: AsyncSession):
        self._session = session

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=UUID(model.id) if isinstance(model.id, str) else model.id,
            email=model.email,
            hashed_password=model.hashed_password,
            full_name=model.full_name,
            role=UserRole(model.role),
            is_active=model.is_active,
            created_at=model.created_at,
        )

    def _to_model(self, entity: User) -> UserModel:
        return UserModel(
            id=str(entity.id),
            email=entity.email,
            hashed_password=entity.hashed_password,
            full_name=entity.full_name,
            role=entity.role.value if isinstance(entity.role, UserRole) else entity.role,
            is_active=entity.is_active,
            created_at=entity.created_at,
        )

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        result = await self._session.get(UserModel, str(user_id))
        return self._to_entity(result) if result else None

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        return self._to_entity(row) if row else None

    async def create(self, user: User) -> User:
        model = self._to_model(user)
        self._session.add(model)
        await self._session.flush()
        return self._to_entity(model)

    async def update(self, user: User) -> User:
        model = await self._session.get(UserModel, str(user.id))
        if model:
            model.email = user.email
            model.full_name = user.full_name
            model.role = user.role.value if isinstance(user.role, UserRole) else user.role
            model.is_active = user.is_active
            await self._session.flush()
        return self._to_entity(model)
