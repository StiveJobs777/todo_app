from abc import abstractmethod
from typing import TYPE_CHECKING

from archtool.layers.default_layer_interfaces import ABCController, ABCRepo, ABCService
from web_fractal.http.interfaces import HttpControllerABC
from sqlalchemy.ext.asyncio import AsyncSession

from .dtos import CreateTodoDTO
from .dms import TodoDM

if TYPE_CHECKING:
    from app.todos.models import TodoORM


class TodoRepoABC(ABCRepo):
    """Data access for Todos."""

    @abstractmethod
    async def create_todo(self, session: AsyncSession, dto: CreateTodoDTO) -> "TodoORM":
        """Create a todo. Raises nothing (user existence checked by service)."""
        ...

    @abstractmethod
    async def get_todo_by_id(self, session: AsyncSession, todo_id: int) -> "TodoORM":
        """Get todo by id. Raises TodoNotFound if missing."""
        ...

    @abstractmethod
    async def list_todos_for_user(self, session: AsyncSession, user_id: int) -> list["TodoORM"]:
        """List all todos for a user."""
        ...


class TodoServiceABC(ABCService):
    """Business logic for Todos."""

    @abstractmethod
    async def create_todo(self, session: AsyncSession, dto: CreateTodoDTO) -> "TodoORM":
        """Validate user exists, then create todo."""
        ...


class TodoControllerABC(ABCController, HttpControllerABC):
    """HTTP API for Todos."""

    @abstractmethod
    async def create_todo(self, payload: CreateTodoDTO) -> TodoDM: ...

    @abstractmethod
    async def list_todos(self, user_id: int) -> list[TodoDM]: ...

    @abstractmethod
    async def complete_todo(self, todo_id: int) -> TodoDM: ...
