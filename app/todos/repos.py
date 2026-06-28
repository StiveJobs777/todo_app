from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .dtos import CreateTodoDTO
from .exceptions import TodoNotFound
from .interfaces import TodoRepoABC
from .models import TodoORM


class TodoRepo(TodoRepoABC):

    async def create_todo(self, session: AsyncSession, dto: CreateTodoDTO) -> TodoORM:
        todo = TodoORM(title=dto.title, user_id=dto.user_id)
        session.add(todo)
        await session.flush()
        await session.refresh(todo)
        return todo

    async def get_todo_by_id(self, session: AsyncSession, todo_id: int) -> TodoORM:
        todo = await session.get(TodoORM, todo_id)
        if todo is None:
            raise TodoNotFound(todo_id)
        return todo

    async def list_todos_for_user(self, session: AsyncSession, user_id: int) -> list[TodoORM]:
        result = await session.execute(select(TodoORM).where(TodoORM.user_id == user_id))
        return list(result.scalars().all())
