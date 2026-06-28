from sqlalchemy.ext.asyncio import AsyncSession

from app.users.interfaces import UserServiceABC  # cross-module dependency

from .dtos import CreateTodoDTO
from .interfaces import TodoRepoABC, TodoServiceABC
from .models import TodoORM


class TodoService(TodoServiceABC):
    todo_repo: TodoRepoABC
    user_service: UserServiceABC  # injected cross-module dependency

    async def create_todo(self, session: AsyncSession, dto: CreateTodoDTO) -> TodoORM:
        # Validate user exists (uses cross-domain UserService)
        await self.user_service.get_user(session, dto.user_id)
        return await self.todo_repo.create_todo(session, dto)
