from abc import abstractmethod

from archtool.layers.default_layer_interfaces import ABCController, ABCRepo, ABCService
from web_fractal.http.interfaces import HttpControllerABC
from sqlalchemy.ext.asyncio import AsyncSession

from .dtos import CreateUserDTO
from .dms import UserDM


class UserRepoABC(ABCRepo):
    """Data access for Users."""

    @abstractmethod
    async def create_user(self, session: AsyncSession, dto: CreateUserDTO) -> "UserORM":
        """Create and persist a user. Raises UserConflictError if email taken."""
        ...

    @abstractmethod
    async def get_user_by_id(self, session: AsyncSession, user_id: int) -> "UserORM":
        """Get user by id. Raises UserNotFound if missing."""
        ...


class UserServiceABC(ABCService):
    """Business logic for Users."""

    @abstractmethod
    async def get_user(self, session: AsyncSession, user_id: int) -> "UserORM":
        """Return user or raise UserNotFound."""
        ...


class UserControllerABC(ABCController, HttpControllerABC):
    """HTTP API for Users."""

    @abstractmethod
    async def create_user(self, payload: CreateUserDTO) -> UserDM: ...

    @abstractmethod
    async def get_user(self, user_id: int) -> UserDM: ...
