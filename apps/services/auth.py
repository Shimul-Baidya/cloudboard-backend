# authentication logic
from sqlalchemy import false
from starlette.status import HTTP_401_UNAUTHORIZED
from apps.database import get_db
from sqlalchemy.orm import Session
from apps.models import user as user_model
from fastapi import HTTPException, status
from apps.services.security import DUMMY_HASH, verify_password
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(db: Session, email: str):
    user = db.query(user_model.User).filter(user_model.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user(db, email)
    if not user:
        verify_password(password, DUMMY_HASH)
        return false
    if not verify_password(password, user.hashed_password):
        return false
    return user
    

    


# exceptions

def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return credentials_exception

def token_exception():
    token_exception_response = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return token_exception_response
