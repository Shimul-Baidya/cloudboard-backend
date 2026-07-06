from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from starlette.status import HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from apps.models import user as user_model
from apps.schemas import user as user_schema
from apps.database import get_db
from apps.services.security import get_password_hash
from apps.services.auth import get_current_user, require_roles
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/user/register", response_model=user_schema.UserResponse)
def create_user(user: user_schema.CreateUser, db: Session = Depends(get_db)):
    logger.info('POST request to /users')
    if db.query(user_model.User).filter(user_model.User.email == user.email).first():
        logger.warning('Email already exists in database')
        raise HTTPException(status_code=409, detail="Email already exists!")
    
    # get the hashed password
    hashed_password = get_password_hash(user.password)
    # create a new user
    new_user = user_model.User(
        email = user.email,
        hashed_password = hashed_password,
        role = user.role
    )

    # # Not tested
    # # creating a user using model_dump()
    # user_data = user.model_dump(exclude={"password"})
    # user_data["hashed_password"] = get_password_hash(user.password)
    # new_user = user_model.User(**user_data)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info('New user created')
    return new_user


@router.get("/users/me", response_model=user_schema.UserResponse)
async def read_user_me(current_user: Annotated[user_model.User, Depends(get_current_user)]):
    logger.info('GET request to /users/me')
    return current_user


@router.get("/users/id/{user_id}", response_model=user_schema.UserResponse)
def get_user_by_id(
    user_id: int, db: Session = Depends(get_db), 
    current_user: user_model.User = Depends(require_roles(["admin"]))
    ):
    logger.info(f'GET request to /users/id/{user_id}')
    user = db.query(user_model.User).filter(user_model.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/delete_user/{user_id}")
def delete_user_by_id(
    user_id: int, db: Session = Depends(get_db),
    current_user: user_model.User = Depends(require_roles(["admin"]))
    ):
    logger.info(f'DELETE request to /delete_user/{user_id}')
    user = db.query(user_model.User).filter(user_model.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    logger.info(f'User deleted: user id {user_id}')
    return Response(status_code=HTTP_204_NO_CONTENT)


# update user route needed