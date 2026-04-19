from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CreateUser(BaseModel):
    email: str
    hashed_password: Optional[str] = None # this is not provided when calling CreateUser
                                          # this will be created inside the specific endpoint
    password: str
    role: str = "user"

class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True