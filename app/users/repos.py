from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from .dtos import CreateUserDTO
from .exceptions import UserNotFound, UserConflictError
from .interfaces import UserRepoABC
from .models import UserORM


class UserRepo(UserRepoABC):

    async def create_user(self, session: AsyncSession, dto: CreateUserDTO) -> UserORM:
        user = UserORM(email=dto.email, name=dto.name)
        session.add(user)
        try:
            await session.flush()
        except IntegrityError:
            await session.rollback()
            raise UserConflictError(dto.email)
        await session.refresh(user)
        return user

    async def get_user_by_id(self, session: AsyncSession, user_id: int) -> UserORM:
        user = await session.get(UserORM, user_id)
        if user is None:
            raise UserNotFound(user_id)
        return user
