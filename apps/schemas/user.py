from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CreateUser(BaseModel):
    email: str
    password: str
    role: str = "user"

class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True