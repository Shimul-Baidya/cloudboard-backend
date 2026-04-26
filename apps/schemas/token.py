from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

# schema for JWT payload
class TokenData(BaseModel):
    email: str | None = None
