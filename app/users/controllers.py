from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import async_sessionmaker

from web_fractal.db import UnitOfWork
from web_fractal.utils import serialize

from .dtos import CreateUserDTO
from .dms import UserDM
from .exceptions import UserNotFound, UserConflictError
from .interfaces import UserControllerABC, UserRepoABC


class UserController(UserControllerABC):
    router = APIRouter(prefix="/users", tags=["users"])
    session_maker: async_sessionmaker
    user_repo: UserRepoABC

    def init_http_routes(self) -> None:
        self.reg_route(self.create_user, methods=["POST"])
        self.reg_route(self.get_user, methods=["GET"], path="/{user_id}")

    async def create_user(self, payload: CreateUserDTO) -> UserDM:
        async with UnitOfWork(self.session_maker) as uow:
            session = uow.get_session()
            try:
                user = await self.user_repo.create_user(session, payload)
                await session.commit()
            except UserConflictError as exc:
                raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
            return serialize(UserDM, user, as_list=False)

    async def get_user(self, user_id: int) -> UserDM:
        async with UnitOfWork(self.session_maker) as uow:
            session = uow.get_session()
            try:
                user = await self.user_repo.get_user_by_id(session, user_id)
            except UserNotFound:
                raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
            return serialize(UserDM, user, as_list=False)
