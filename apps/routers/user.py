from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.models import user as user_model
from apps.schemas import user as user_schema
from apps.database import get_db
from apps.services.security import get_password_hash
from apps.services.auth import get_current_user


router = APIRouter()

@router.post("/users", response_model=user_schema.UserResponse)
def create_user(user: user_schema.CreateUser, db: Session = Depends(get_db)):
    if db.query(user_model.User).filter(user_model.User.email == user.email).first(): 
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
    return new_user


@router.get("/users/me", response_model=user_schema.UserResponse)
async def read_user_me(current_user: Annotated[user_model.User, Depends(get_current_user)]):
    return current_user


@router.get("/users/id/{user_id}", response_model=user_schema.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user