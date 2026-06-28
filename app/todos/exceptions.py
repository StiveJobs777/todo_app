class TodoError(Exception):
    """Base todo domain exception."""


class TodoNotFound(TodoError):
    def __init__(self, todo_id: int):
        self.todo_id = todo_id
        super().__init__(f"Todo {todo_id} not found")
