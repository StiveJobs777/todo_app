class UserError(Exception):
    """Base user domain exception."""


class UserNotFound(UserError):
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User {user_id} not found")


class UserConflictError(UserError):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email={email} already exists")
