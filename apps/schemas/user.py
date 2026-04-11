from pydantic import BaseModel

class CreateUser(BaseModel):
    email: str
    hashed_password: str
    role: str = "user"

class UserResponse(BaseModel):
    id: int
    email: str
    role: str

    class Config:
        from_attributes = True