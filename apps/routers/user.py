from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.models import user as user_model
from apps.schemas import user as user_schema
from apps.database import get_db


router = APIRouter()

@router.post("/users", response_model=user_schema.UserResponse)
def create_user(user: user_schema.CreateUser, db: Session = Depends(get_db)):
    if db.query(user_model.User).filter(user_model.User.email == user.email).first(): 
        raise HTTPException(status_code=409, detail="Email already exists!")
    
    # create a new user
    new_user = user_model.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/{user_id}", response_model=user_schema.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
