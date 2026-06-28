from pydantic import BaseModel


class TodoDM(BaseModel):
    id: int
    title: str
    completed: bool
    user_id: int

    model_config = {"from_attributes": True}
