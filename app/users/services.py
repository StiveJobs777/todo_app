from sqlalchemy.ext.asyncio import AsyncSession

from .interfaces import UserRepoABC, UserServiceABC
from .models import UserORM


class UserService(UserServiceABC):
    user_repo: UserRepoABC

    async def get_user(self, session: AsyncSession, user_id: int) -> UserORM:
        return await self.user_repo.get_user_by_id(session, user_id)
