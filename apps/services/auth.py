# authentication logic
from starlette.status import HTTP_401_UNAUTHORIZED
from apps.database import get_db
from sqlalchemy.orm import Session
from apps.models import user as user_model
from fastapi import HTTPException, status, Depends
from apps.services.security import ALGORITHM, DUMMY_HASH, SECRET_KEY, verify_password
from apps.schemas.token import TokenData
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(db: Session, email: str):
    user = db.query(user_model.User).filter(user_model.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user(db, email) # TODO: How does it work, I have to look this up
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
    

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception()
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception()
    user = get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception()
    return user




# exceptions

def credentials_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return credentials_exception

def token_exception():
    token_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return token_exception
