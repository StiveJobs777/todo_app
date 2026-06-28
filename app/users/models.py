from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from web_fractal.db import Base

if TYPE_CHECKING:
    from app.todos.models import TodoORM


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))

    todos: Mapped[list["TodoORM"]] = relationship("TodoORM", back_populates="user")
