from pydantic import BaseModel


class UserDM(BaseModel):
    id: int
    email: str
    name: str

    model_config = {"from_attributes": True}
