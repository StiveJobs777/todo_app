from pydantic import BaseModel, EmailStr


class CreateUserDTO(BaseModel):
    email: str
    name: str
