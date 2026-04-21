# authentication logic
from sqlalchemy import false
from apps.database import get_db
from sqlalchemy.orm import Session
from apps.models import user as user_model
from fastapi import HTTPException
from apps.services.security import DUMMY_HASH, verify_password


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
    

    


