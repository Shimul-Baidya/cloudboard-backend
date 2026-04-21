# hashing + JWT
from datetime import timedelta, datetime, timezone
from pydantic import BaseModel
from pwdlib import PasswordHash
import jwt

SECRET_KEY = "7e6eca543daca05da7bf972edc276c7cde8340060730cb0d4bb6c329cefbfba8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 

class Token(BaseModel):
    access_token: str
    token_type: str

password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummypassword")

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt