from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import async_sessionmaker

from web_fractal.db import UnitOfWork
from web_fractal.utils import serialize

from app.users.exceptions import UserNotFound

from .dtos import CreateTodoDTO
from .dms import TodoDM
from .exceptions import TodoNotFound
from .interfaces import TodoControllerABC, TodoRepoABC, TodoServiceABC


class TodoController(TodoControllerABC):
    router = APIRouter(prefix="/todos", tags=["todos"])
    session_maker: async_sessionmaker
    todo_repo: TodoRepoABC
    todo_service: TodoServiceABC

    def init_http_routes(self) -> None:
        self.reg_route(self.create_todo, methods=["POST"])
        self.reg_route(self.list_todos, methods=["GET"])
        self.reg_route(self.complete_todo, methods=["PATCH"], path="/{todo_id}/complete_todo")

    async def create_todo(self, payload: CreateTodoDTO) -> TodoDM:
        async with UnitOfWork(self.session_maker) as uow:
            session = uow.get_session()
            try:
                todo = await self.todo_service.create_todo(session, payload)
                await session.commit()
            except UserNotFound:
                raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
            return serialize(TodoDM, todo, as_list=False)

    async def list_todos(self, user_id: int) -> list[TodoDM]:
        async with UnitOfWork(self.session_maker) as uow:
            session = uow.get_session()
            todos = await self.todo_repo.list_todos_for_user(session, user_id)
            return serialize(TodoDM, todos, as_list=True)

    async def complete_todo(self, todo_id: int) -> TodoDM:
        async with UnitOfWork(self.session_maker) as uow:
            session = uow.get_session()
            try:
                todo = await self.todo_repo.get_todo_by_id(session, todo_id)
            except TodoNotFound:
                raise HTTPException(status.HTTP_404_NOT_FOUND, "Todo not found")
            todo.completed = True
            session.add(todo)
            await session.commit()
            await session.refresh(todo)
            return serialize(TodoDM, todo, as_list=False)
